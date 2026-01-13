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
```

Use `-y` flag to skip confirmation prompts.

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

The `compile.py` script automatically adds Release/Due lines to the schedule based on this JSON. Do NOT put project info in `meta.txt` files.

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
- `github2`: Update semester reference (e.g., `f23` → `s26`)
- `canvas`: Update Canvas course ID (ask instructor for new ID)

### Step 3: Update schedule.json

- `holiday`: Update entries for the new semester (see below)
- `quizzes`: Ask instructor if online quizzes are being used; set to `[]` if not
- `projects`: Update release/due lecture numbers based on new schedule (see "Project Schedule" section above)

### Step 4: Update syllabus.content.html

- Clear the revision history (set to "none yet" or similar)
- Update final exam date/time (search for "exam 3" or "finals week")
- Ask instructor about any changes to course components (quizzes, projects, etc.)

### Step 5: Ask Instructor About Changes

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
- Space midterms roughly evenly throughout the semester
- Use `claude_util.py create <pos> midterm --midterm` to create midterm lectures with red styling
- Midterm lectures should have `meta.txt` containing: `<h4 style="color: red;">In-Class Midterm</h4>`

### Step 6: Build and Verify

```bash
python3 compile.py
```

Verify:
- No errors
- Schedule shows MWF columns (not WFM or other order)
- Correct number of class days
- Holidays appear correctly

### Semester-Specific Holidays (MWF classes)

**Fall semesters:**
- Labor Day (first Monday of September) - START_DATE should be this Monday
- Thanksgiving Break (W and F of Thanksgiving week, possibly all 3 days)

**Spring semesters:**
- MLK Day (third Monday of January) - START_DATE should be this Monday
- Spring Break (M, W, F of spring break week)