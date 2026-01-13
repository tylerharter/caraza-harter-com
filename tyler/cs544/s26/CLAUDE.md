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

- **schedule.json**: Defines course sections, holidays, and quiz weeks
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

## Setting Up a New Semester

When copying a previous semester to create a new one, update the following:

### Academic Calendar
Fetch dates from: https://secfac.wisc.edu/academic-calendar/

### Files to Update

**compile.py:**
- `START_DATE`: Must be a **Monday** for correct MWF column order (even if that Monday is a holiday)
- `CUTOFF_DATE` and `END_DATE`: Last day of instruction
- `github`: Update semester in URL (e.g., `f25` → `s26`)
- `github2`: Update semester reference
- `canvas`: Update Canvas course ID

**schedule.json:**
- Update `holiday` entries for the new semester

### Semester-Specific Holidays (MWF classes)

**Fall semesters:**
- Labor Day (first Monday of September) - START_DATE should be this Monday
- Thanksgiving Break (Wednesday and Friday of Thanksgiving week)

**Spring semesters:**
- MLK Day (third Monday of January) - START_DATE should be this Monday
- Spring Break (M, W, F of spring break week)