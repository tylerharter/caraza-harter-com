#!/usr/bin/env python3
"""Utility script for Claude to manage course content efficiently."""

import argparse
import os
import re
import subprocess
import sys

LEC_DIR = "lec"

def get_lectures():
    """Return sorted list of lecture directories matching NN-name pattern."""
    if not os.path.exists(LEC_DIR):
        return []
    dirs = [d for d in os.listdir(LEC_DIR) if re.match(r"\d\d-.*", d)]
    return sorted(dirs)

def parse_lecture_dir(dirname):
    """Parse lecture directory name into (number, name) tuple."""
    match = re.match(r"(\d\d)-(.+)", dirname)
    if match:
        return int(match.group(1)), match.group(2)
    return None, None

def find_lecture(lectures, target):
    """Find a lecture by number or name pattern. Returns (index, dirname) or (None, None)."""
    for i, lec in enumerate(lectures):
        num, name = parse_lecture_dir(lec)
        if str(num) == str(target) or str(target).lower() in lec.lower():
            return i, lec
    return None, None

def run_git(args, check=True, force=False):
    """Run a git command and return output."""
    if force and args[0] == "rm":
        args = [args[0], "-f"] + args[1:]
    cmd = ["git"] + args
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def renumber_range(lectures, start_idx, end_idx, delta):
    """Renumber lectures in a range by delta. Works in correct order to avoid conflicts."""
    if delta > 0:
        # Moving up: process in reverse to avoid conflicts
        indices = range(end_idx - 1, start_idx - 1, -1)
    else:
        # Moving down: process forward
        indices = range(start_idx, end_idx)

    for i in indices:
        old_dir = lectures[i]
        old_num, name = parse_lecture_dir(old_dir)
        new_num = old_num + delta
        new_dir = f"{new_num:02d}-{name}"

        if old_dir != new_dir:
            old_path = os.path.join(LEC_DIR, old_dir)
            new_path = os.path.join(LEC_DIR, new_dir)
            run_git(["mv", old_path, new_path])

def cmd_list(args):
    """List all lectures."""
    lectures = get_lectures()
    for lec in lectures:
        num, name = parse_lecture_dir(lec)
        meta_path = os.path.join(LEC_DIR, lec, "meta.txt")
        desc = ""
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                desc = f.read().strip().split('\n')[0][:50]
        print(f"{num:2d}. {name:20s} {desc}")

def cmd_delete(args):
    """Delete a lecture and renumber subsequent lectures."""
    lectures = get_lectures()
    target_idx, target_dir = find_lecture(lectures, args.lecture)

    if target_dir is None:
        print(f"Error: Could not find lecture matching '{args.lecture}'")
        sys.exit(1)

    print(f"Will delete: {target_dir}")
    print(f"Will renumber {len(lectures) - target_idx - 1} subsequent lectures")

    if not args.yes:
        confirm = input("Proceed? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    # Delete the target lecture
    target_path = os.path.join(LEC_DIR, target_dir)
    run_git(["rm", "-r", target_path], force=True)

    # Renumber subsequent lectures (shift down by 1)
    renumber_range(lectures, target_idx + 1, len(lectures), -1)

def cmd_insert(args):
    """Insert space for a new lecture by shifting subsequent lectures up."""
    lectures = get_lectures()
    position = int(args.position)

    # Find lectures that need to move
    start_idx = None
    for i, lec in enumerate(lectures):
        num, _ = parse_lecture_dir(lec)
        if num >= position:
            start_idx = i
            break

    if start_idx is None:
        print(f"No lectures at or after position {position}")
        return

    print(f"Will shift {len(lectures) - start_idx} lectures up by 1")

    if not args.yes:
        confirm = input("Proceed? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    # Renumber (shift up by 1)
    renumber_range(lectures, start_idx, len(lectures), +1)
    print(f"\nPosition {position:02d} is now available for a new lecture.")

def cmd_move(args):
    """Move a lecture from one position to another."""
    lectures = get_lectures()
    from_idx, from_dir = find_lecture(lectures, args.source)

    if from_dir is None:
        print(f"Error: Could not find lecture matching '{args.source}'")
        sys.exit(1)

    from_num, from_name = parse_lecture_dir(from_dir)
    to_pos = int(args.dest)

    if from_num == to_pos:
        print("Source and destination are the same. Nothing to do.")
        return

    print(f"Will move: {from_dir} from position {from_num} to position {to_pos}")

    if not args.yes:
        confirm = input("Proceed? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    # Strategy:
    # 1. Temporarily rename the source to a temp name
    # 2. Shift lectures to make room
    # 3. Rename temp to final position

    temp_dir = f"99-{from_name}"
    temp_path = os.path.join(LEC_DIR, temp_dir)
    from_path = os.path.join(LEC_DIR, from_dir)

    # Move to temp
    run_git(["mv", from_path, temp_path])

    # Refresh lectures list (without the moved one)
    lectures = get_lectures()

    if from_num < to_pos:
        # Moving forward: shift lectures between (from+1, to] down by 1
        for i, lec in enumerate(lectures):
            num, name = parse_lecture_dir(lec)
            if from_num < num <= to_pos:
                new_num = num - 1
                new_dir = f"{new_num:02d}-{name}"
                old_path = os.path.join(LEC_DIR, lec)
                new_path = os.path.join(LEC_DIR, new_dir)
                run_git(["mv", old_path, new_path])
    else:
        # Moving backward: shift lectures between [to, from) up by 1
        # Process in reverse to avoid conflicts
        to_shift = [(i, lec) for i, lec in enumerate(lectures)
                    if to_pos <= parse_lecture_dir(lec)[0] < from_num]
        for i, lec in reversed(to_shift):
            num, name = parse_lecture_dir(lec)
            new_num = num + 1
            new_dir = f"{new_num:02d}-{name}"
            old_path = os.path.join(LEC_DIR, lec)
            new_path = os.path.join(LEC_DIR, new_dir)
            run_git(["mv", old_path, new_path])

    # Move from temp to final position
    final_dir = f"{to_pos:02d}-{from_name}"
    final_path = os.path.join(LEC_DIR, final_dir)
    run_git(["mv", temp_path, final_path])

    print(f"Moved {from_name} to position {to_pos}")

def cmd_create(args):
    """Create a new lecture at a position (shifts others if needed)."""
    lectures = get_lectures()
    position = int(args.position)
    name = args.name

    # Check if position exists
    existing_idx, existing_dir = find_lecture(lectures, position)

    if existing_dir is not None:
        print(f"Position {position} is occupied by {existing_dir}")
        print(f"Will shift {len(lectures) - existing_idx} lectures up")

    if not args.yes:
        confirm = input("Proceed? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    # Shift if needed
    if existing_dir is not None:
        # Find start index for shifting
        start_idx = existing_idx
        renumber_range(lectures, start_idx, len(lectures), +1)

    # Create the new lecture
    new_dir = f"{position:02d}-{name}"
    new_path = os.path.join(LEC_DIR, new_dir)
    os.makedirs(new_path, exist_ok=True)

    # Create meta.txt with optional content
    meta_path = os.path.join(new_path, "meta.txt")
    if args.midterm:
        content = '<h4 style="color: red;">In-Class Midterm</h4>\n'
    else:
        content = f'{name}\n'

    with open(meta_path, 'w') as f:
        f.write(content)

    run_git(["add", new_path])
    print(f"Created {new_dir}")

def cmd_rename(args):
    """Rename a lecture (change its topic name, not number)."""
    lectures = get_lectures()
    target_idx, target_dir = find_lecture(lectures, args.lecture)

    if target_dir is None:
        print(f"Error: Could not find lecture matching '{args.lecture}'")
        sys.exit(1)

    target_num, _ = parse_lecture_dir(target_dir)
    new_dir = f"{target_num:02d}-{args.new_name}"
    print(f"Will rename: {target_dir} -> {new_dir}")

    if not args.yes:
        confirm = input("Proceed? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    old_path = os.path.join(LEC_DIR, target_dir)
    new_path = os.path.join(LEC_DIR, new_dir)
    run_git(["mv", old_path, new_path])

def cmd_swap(args):
    """Swap two lectures' positions."""
    lectures = get_lectures()
    idx_a, dir_a = find_lecture(lectures, args.lecture_a)
    idx_b, dir_b = find_lecture(lectures, args.lecture_b)

    if dir_a is None:
        print(f"Error: Could not find lecture matching '{args.lecture_a}'")
        sys.exit(1)
    if dir_b is None:
        print(f"Error: Could not find lecture matching '{args.lecture_b}'")
        sys.exit(1)

    num_a, name_a = parse_lecture_dir(dir_a)
    num_b, name_b = parse_lecture_dir(dir_b)

    print(f"Will swap: {dir_a} <-> {dir_b}")

    if not args.yes:
        confirm = input("Proceed? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    # Use temp directory for swap
    temp_dir = "99-temp-swap"
    path_a = os.path.join(LEC_DIR, dir_a)
    path_b = os.path.join(LEC_DIR, dir_b)
    temp_path = os.path.join(LEC_DIR, temp_dir)

    new_dir_a = f"{num_a:02d}-{name_b}"
    new_dir_b = f"{num_b:02d}-{name_a}"
    new_path_a = os.path.join(LEC_DIR, new_dir_a)
    new_path_b = os.path.join(LEC_DIR, new_dir_b)

    run_git(["mv", path_a, temp_path])
    run_git(["mv", path_b, new_path_b])
    run_git(["mv", temp_path, new_path_a])

    print(f"Swapped {name_a} and {name_b}")

def main():
    parser = argparse.ArgumentParser(description="Course management utilities for Claude")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompts")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list command
    list_parser = subparsers.add_parser("list", help="List all lectures")
    list_parser.set_defaults(func=cmd_list)

    # delete command
    del_parser = subparsers.add_parser("delete", help="Delete a lecture and renumber")
    del_parser.add_argument("lecture", help="Lecture number or name pattern to delete")
    del_parser.set_defaults(func=cmd_delete)

    # insert command
    ins_parser = subparsers.add_parser("insert", help="Make space for a new lecture")
    ins_parser.add_argument("position", help="Position number for new lecture")
    ins_parser.set_defaults(func=cmd_insert)

    # move command
    move_parser = subparsers.add_parser("move", help="Move a lecture to a new position")
    move_parser.add_argument("source", help="Lecture number or name pattern to move")
    move_parser.add_argument("dest", help="Destination position number")
    move_parser.set_defaults(func=cmd_move)

    # create command
    create_parser = subparsers.add_parser("create", help="Create a new lecture at a position")
    create_parser.add_argument("position", help="Position number for new lecture")
    create_parser.add_argument("name", help="Topic name for the lecture")
    create_parser.add_argument("--midterm", action="store_true", help="Create as midterm (red styling)")
    create_parser.set_defaults(func=cmd_create)

    # rename command
    ren_parser = subparsers.add_parser("rename", help="Rename a lecture topic")
    ren_parser.add_argument("lecture", help="Lecture number or name pattern")
    ren_parser.add_argument("new_name", help="New topic name (without number prefix)")
    ren_parser.set_defaults(func=cmd_rename)

    # swap command
    swap_parser = subparsers.add_parser("swap", help="Swap two lectures' positions")
    swap_parser.add_argument("lecture_a", help="First lecture number or name pattern")
    swap_parser.add_argument("lecture_b", help="Second lecture number or name pattern")
    swap_parser.set_defaults(func=cmd_swap)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
