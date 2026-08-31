# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

This is a course website for CS 544 "Intro to Big Data Systems" at UW-Madison. The codebase is a static site generator that creates HTML pages for the course schedule, syllabus, and other course materials.

### Core Components

- **compile.py**: Main build script that generates the course website
  - Reads lecture metadata from `lec/*/meta.txt` files
  - Processes `schedule.json` for course structure
  - Generates HTML files from `.content.html` templates using `template.html`
  - Links to slides, worksheets, and other materials in lecture directories

- **Template System**: 
  - `template.html`: Base HTML template with Bootstrap styling
  - `*.content.html`: Content files that get inserted into the template
  - Generated `*.html`: Final pages (schedule.html, syllabus.html, etc.)

- **Lecture Structure**: Each lecture in `lec/NN-topic/` contains:
  - `meta.txt`: Lecture description and metadata
  - `slides.key`: Keynote slides (exported to PDF for web)
  - `worksheet.pages`: Worksheets (exported to PDF)
  - `anki.apkg`: Anki flashcard decks

### Configuration Files

- **schedule.json**: Defines course sections, holidays, quizzes, and project schedule
- **Static Assets**: CSS in `css/`, JavaScript in `js/`, images in `img/`

### Related Files (Other Repos)

- **Projects policy**: `/Users/tharter/g/s26/projects.md` - Contains project submission policies, late policy, grade disputes, etc. This file and `syllabus.content.html` together define all course policies tested in the Canvas policy quiz.

## Common Commands

### Build the Website
```bash
python3 compile.py
```
This processes all content and generates the final HTML files.

### Development Workflow
1. Edit content in `*.content.html` files or lecture `meta.txt` files
2. Run `python3 compile.py` to regenerate HTML
3. Open generated HTML files in browser to preview

### Adding New Lectures
1. Create new directory `lec/NN-topic/` (where NN is zero-padded number)
2. Add `meta.txt` with lecture description
3. Add slides, worksheets, or other materials as needed
4. Run compile script to update schedule

## File Naming Conventions

- Lecture directories: `NN-topic` (e.g., `01-course`, `02-shell`)
- Content files: `name.content.html` → generates `name.html`
- JavaScript: `js/name.js` is automatically included if it exists for `name.html`

## Lecture Management (claude_util.py)

Utility script for managing lectures efficiently:

```bash
# List all lectures with descriptions
python3 claude_util.py list

# Delete a lecture and renumber all subsequent lectures
python3 claude_util.py delete <number-or-pattern>
python3 claude_util.py -y delete grpc-catchup  # skip confirmation

# Insert space for a new lecture (shifts subsequent lectures up)
python3 claude_util.py insert <position>

# Move a lecture to a new position (shifts others accordingly)
python3 claude_util.py move <source> <dest>
python3 claude_util.py -y move 9 7  # move lecture 9 to position 7

# Create a new lecture at a position (shifts others if needed)
python3 claude_util.py create <position> <name>
python3 claude_util.py create 7 midterm --midterm  # creates with red styling

# Rename a lecture topic (keeps the number)
python3 claude_util.py rename <number-or-pattern> <new-name>

# Swap two lectures' positions
python3 claude_util.py swap <lecture_a> <lecture_b>

# Remove all video recording links from meta.txt files (for new semester)
python3 claude_util.py clear-videos
```

Use `-y` flag to skip confirmation prompts.

## Canvas Integration (claude_util.py)

Canvas commands require an API token. Store your token in `~/auth/canvas.txt` or set the `CANVAS_TOKEN` environment variable. Get a token from Canvas → Account → Settings → New Access Token.

These commands require the venv: `source venv/bin/activate`

```bash
# Sync project and midterm deadlines to Canvas
# Creates assignments as unpublished drafts with "No Submission" type
# Points should be read from syllabus.content.html before running
python3 claude_util.py -y canvas-sync --project-points 3 --midterm-points 12

# Download a Canvas quiz as markdown with answers
python3 claude_util.py canvas-quiz "https://canvas.wisc.edu/courses/COURSE_ID/quizzes/QUIZ_ID"
python3 claude_util.py canvas-quiz "URL" > quiz.md  # save to file
```

**canvas-sync details:**
- Reads project due dates from `schedule.json` (by lecture number)
- Finds midterms by scanning `lec/*/` for directories containing "midterm"
- Projects are due at 11:59 PM on the lecture date
- Midterms are due at 8:00 AM on the lecture date
- Creates assignments as unpublished drafts

**canvas-quiz details:**
- Outputs quiz as markdown with questions and answers
- Correct answers marked with ✓, incorrect with ○ or ☐
- Supports multiple choice, true/false, multiple answers, short answer, fill-in-the-blank, matching, numerical, and essay questions

## Project Schedule (schedule.json)

Projects are defined in `schedule.json` under the `projects` key. Each project specifies:
- `release`: Lecture number when project is released
- `due`: Lecture number when project is due
- `title`: Short description shown in parentheses

Example:
```json
{
  "projects": {
    "P1": {"release": 4, "due": 10, "title": "Docker"},
    "P2": {"release": 10, "due": 16, "title": "Network+Memory"},
    ...
  }
}
```

**Guidelines for project scheduling:**
- Prefer Wednesday releases and due dates when possible
- Avoid due dates right before or after spring break
- P8 should be due on the last day of class
- Allow at least 1 week per project (P8 needs exactly 1 week)
- Projects crossing spring break can have longer durations
- **Always pair Due of PN with Release of P(N+1)** on the same lecture
- Use single-word titles (e.g., "Docker", "Spark", "Kafka") or simple combinations (e.g., "Network+Memory")

The `compile.py` script automatically adds Release/Due lines to the schedule based on this JSON. Do NOT put project info in `meta.txt` files.

## Worksheet Schedule (schedule.json)

Worksheets are defined in `schedule.json` under the `"worksheets"` key. Each worksheet specifies only a due date (no release date). The key is the worksheet name (displayed as "{Name} Worksheet" on the schedule, lowercased for the PDF filename).

Example:
```json
{
  "worksheets": {
    "Shell": {"due": 6},
    "Git": {"due": 8}
  }
}
```

- `due`: Lecture number when the worksheet is due
- The link points to `handin-worksheets/{name_lower}.pdf` on GitLab

The `compile.py` script automatically adds "Due:" lines to the schedule based on this JSON.

## Setting Up a New Semester

When copying a previous semester to create a new one, follow this checklist. Claude should be able to handle most of this autonomously, asking the instructor questions as needed.

### Step 1: Fetch Academic Calendar
Get dates from: https://secfac.wisc.edu/academic-calendar/

Look for:
- Instruction begin date
- Spring break dates (spring) or Thanksgiving dates (fall)
- Instruction end date
- Final exam period dates

### Step 2: Update compile.py

- `START_DATE`: Must be a **Monday** for correct MWF column order (even if that Monday is a holiday)
- `CUTOFF_DATE` and `END_DATE`: Last day of instruction
- `github`: Update semester in URL (e.g., `f25` → `s26`)
- `github2`: GitLab URL for project links - update semester (e.g., `s26` in the path)
- `canvas`: Update Canvas course ID (ask instructor for new ID)

### Step 3: Update schedule.json

- `holiday`: Update entries for the new semester (see below)
- `quizzes`: Ask instructor if online quizzes are being used; set to `[]` if not
- `projects`: Update release/due lecture numbers based on new schedule (see "Project Schedule" section above)

### Step 4: Update syllabus.content.html

- Clear the revision history (set to "none yet" or similar)
- Update final exam date/time (search for "exam 3" or "finals week")
- Ask instructor about any changes to course components (quizzes, projects, etc.)

### Step 5: Clear Previous Semester's Video Links

```bash
python3 claude_util.py clear-videos
```

This removes all mediaspace.wisc.edu video recording links from `meta.txt` files, since new recordings will be made for the new semester.

### Step 6: Ask Instructor About Changes

Questions to ask:
- Are there any lectures to delete, add, or rename?
- Are online quizzes being used this semester?
- What is the Canvas course ID?
- What is the final exam date/time?
- How many midterms and when should they be scheduled?
- Any other syllabus changes?

### Midterm Scheduling Guidelines

- First midterm should be in week 3
- No midterms in the last two weeks of the semester
- Place midterms at **content boundaries** (e.g., after networking, after SQL, after Spark)
- Space midterms roughly evenly throughout the semester
- Use `claude_util.py create <pos> midterm --midterm` to create midterm lectures with red styling
- Midterm lectures should have `meta.txt` containing: `<h4 style="color: red;">In-Class Midterm</h4>`

### Step 7: Build and Verify

```bash
python3 compile.py
```

Verify:
- No errors
- Schedule shows MWF columns (not WFM or other order)
- Correct number of class days
- Holidays appear correctly

### Step 8: Sync Canvas Assignments

After the schedule is finalized, sync project and midterm deadlines to Canvas:

```bash
source venv/bin/activate
# Read points from syllabus.content.html first, then run:
python3 claude_util.py -y canvas-sync --project-points <N> --midterm-points <N>
```

This creates assignments as unpublished drafts. The instructor can review and publish them.

### Step 9: Verify Policy Quiz

The policy quiz tests students on policies documented in two places:
- `syllabus.content.html` (this repo)
- `/Users/tharter/g/s26/projects.md` (separate repo)

Download the policy quiz and check for consistency:

```bash
source venv/bin/activate
python3 claude_util.py canvas-quiz "https://canvas.wisc.edu/courses/COURSE_ID/quizzes/QUIZ_ID" > quiz.md
```

Then compare quiz.md against both policy documents:
1. Every policy tested in the quiz should be documented in one of the two files
2. Check for contradictions between quiz answers and documentation
3. Update documentation or quiz as needed to resolve inconsistencies

Common policy areas to verify:
- GitLab submission process (Status: Passed meaning, official scores in Issues)
- Late policy (no grace period, 3-day waiver requirements, no email submissions)
- Grade disputes (contact TA who graded you first)
- Hand-in worksheets (in-person only, due date or next lecture, deduction reasons)
- Email guidelines (CC partner, 2 business days to escalate, single thread for multiple recipients)
- TopHat/extra credit (own section only, enough to miss many and max out, no re-opens)

### Semester-Specific Holidays (MWF classes)

**Fall semesters:**
- Labor Day (first Monday of September) - START_DATE should be this Monday
- Thanksgiving Break (W and F of Thanksgiving week, possibly all 3 days)

**Spring semesters:**
- MLK Day (third Monday of January) - START_DATE should be this Monday
- Spring Break (M, W, F of spring break week)

## Instructor Preferences

**When making changes:**
- Don't change weights of course components (projects, worksheets, etc.) unless explicitly asked
- It's okay if points temporarily don't add to 100 - instructor will fix later
- When verifying project pairings, always check that Due of PN = Release of P(N+1)
- Last lecture should typically be a review day