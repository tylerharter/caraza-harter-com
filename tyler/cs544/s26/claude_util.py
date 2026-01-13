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

def run_git(args, check=True):
    """Run a git command and return output."""
    cmd = ["git"] + args
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

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
    target = args.lecture

    # Find the lecture to delete (by number or name pattern)
    target_dir = None
    target_idx = None

    for i, lec in enumerate(lectures):
        num, name = parse_lecture_dir(lec)
        if str(num) == target or target.lower() in lec.lower():
            target_dir = lec
            target_idx = i
            break

    if target_dir is None:
        print(f"Error: Could not find lecture matching '{target}'")
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
    run_git(["rm", "-r", target_path])

    # Renumber subsequent lectures
    for i in range(target_idx + 1, len(lectures)):
        old_dir = lectures[i]
        old_num, name = parse_lecture_dir(old_dir)
        new_num = old_num - 1
        new_dir = f"{new_num:02d}-{name}"

        if old_dir != new_dir:
            old_path = os.path.join(LEC_DIR, old_dir)
            new_path = os.path.join(LEC_DIR, new_dir)
            run_git(["mv", old_path, new_path])

def cmd_insert(args):
    """Insert space for a new lecture by shifting subsequent lectures up."""
    lectures = get_lectures()
    position = int(args.position)

    # Find lectures that need to move
    to_move = []
    for lec in lectures:
        num, name = parse_lecture_dir(lec)
        if num >= position:
            to_move.append((num, name, lec))

    if not to_move:
        print(f"No lectures at or after position {position}")
        return

    print(f"Will shift {len(to_move)} lectures up by 1")

    if not args.yes:
        confirm = input("Proceed? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    # Renumber in reverse order to avoid conflicts
    for num, name, old_dir in reversed(to_move):
        new_num = num + 1
        new_dir = f"{new_num:02d}-{name}"
        old_path = os.path.join(LEC_DIR, old_dir)
        new_path = os.path.join(LEC_DIR, new_dir)
        run_git(["mv", old_path, new_path])

    print(f"\nPosition {position:02d} is now available for a new lecture.")

def cmd_rename(args):
    """Rename a lecture (change its topic name, not number)."""
    lectures = get_lectures()
    target = args.lecture
    new_name = args.new_name

    # Find the lecture
    target_dir = None
    for lec in lectures:
        num, name = parse_lecture_dir(lec)
        if str(num) == target or target.lower() in lec.lower():
            target_dir = lec
            target_num = num
            break

    if target_dir is None:
        print(f"Error: Could not find lecture matching '{target}'")
        sys.exit(1)

    new_dir = f"{target_num:02d}-{new_name}"
    print(f"Will rename: {target_dir} -> {new_dir}")

    if not args.yes:
        confirm = input("Proceed? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    old_path = os.path.join(LEC_DIR, target_dir)
    new_path = os.path.join(LEC_DIR, new_dir)
    run_git(["mv", old_path, new_path])

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

    # rename command
    ren_parser = subparsers.add_parser("rename", help="Rename a lecture topic")
    ren_parser.add_argument("lecture", help="Lecture number or name pattern")
    ren_parser.add_argument("new_name", help="New topic name (without number prefix)")
    ren_parser.set_defaults(func=cmd_rename)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
