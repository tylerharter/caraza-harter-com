#!/usr/bin/env python3
import calendar, os, json, re
from datetime import date, timedelta

github = 'https://github.com/tylerharter/caraza-harter-com/blob/master/tyler/cs544/f24'
github2 = 'https://github.com/cs544-wisc/f23/tree/main'
canvas = 'https://canvas.wisc.edu/courses/427528'

START_DATE = date(2024, 9, 2)
CUTOFF_DATE = date(2024, 12, 13) # don't show content after this
END_DATE = date(2024, 12, 11)

def template():
    with open('template.html') as f:
        template = f.read()
    suffix = '.content.html'
    for path in os.listdir('.'):
        if path.endswith(suffix):
            with open(path) as f:
                content = f.read()
            name = path[:-len(suffix)]
            new = name + '.html'

            full = template.replace("{CONTENT}", content)
            script = 'js/%s.js' % name
            include = '<script src="%s"></script>'%script if os.path.exists(script) else ''
            full = full.replace("{SCRIPTS}", include)

            print('%s => %s' % (path, new))
            with open(new, 'w') as f:
                f.write(full)

def format_day(day, num):
    lines = [re.sub("#.*", "\n", line) for line in day.split('\n')]
    out = []
    for i,line in enumerate(lines):
        if line.startswith('*'):
            if i==0 or not lines[i-1].startswith('*'):
                out.append('<ul class="compact-ul">')
            out.append('<li>'+line[1:])
            if i==len(lines)-1 or not lines[i+1].startswith('*'):
                out.append('</ul>')
        else:
            out.append(line)
    out[0] = f'<span id="lec-{num}-title">{out[0]}</span>'
    return '\n'.join(out)

def read_days():
    days = []
    for dirname in sorted(os.listdir("lec")):
        m = re.match(r"(\d\d)\-", dirname)
        if not m:
            continue
        num = m.group(1)
        meta = os.path.join("lec", dirname, "meta.txt")
        with open(meta) as f:
            meta = format_day(f.read(), num)
        meta = meta.replace("SLIDES\n", "")

        outline = os.path.join("lec", dirname, "README.md")
        slides = os.path.join("lec", dirname, "slides.pdf")
        if os.path.exists(slides):
            modtime = os.path.getmtime(slides)
            if modtime < 1693327527: # Aug 29, 2023 (from time.time())
                meta += f'\n<b>Old Slides</b>: <a href="{slides}">PDF</a><br>'
            else:
                meta += f'\n<b>Slides</b>: <a href="{slides}">PDF</a><br>'
        worksheet = os.path.join("lec", dirname, "worksheet.pdf")
        if os.path.exists(worksheet):
            modtime = os.path.getmtime(worksheet)
            if modtime < 1693327527: # Aug 29, 2023 (from time.time())
                meta += f'\n<b>Old Worksheet</b>: <a href="{worksheet}">PDF</a><br>'
            else:
                meta += f'\n<b>Worksheet</b>: <a href="{worksheet}">PDF</a><br>'
            answers = os.path.join("lec", dirname, "worksheet-answers.pdf")
            if os.path.exists(answers):
                meta += f' (<a href="{answers}">answers</a>)'
        anki = os.path.join("lec", dirname, "anki.apkg")
        if os.path.exists(anki):
            meta += f'\n<b>Anki Flashcards</b>: <a href="{anki}">Deck</a><br>'
        pt = os.path.join("lec", dirname, "pytutor.html")
        if os.path.exists(pt):
            meta += f'\n<b>PythonTutor</b>: <a href="{pt}">examples</a><br>'
        reading = os.path.join("lec", dirname, "reading.md")
        if os.path.exists(reading):
            meta += f'\n<b>Read</b>: <a href="{github}/{reading}">Course Notes</a><br>'
        reading = os.path.join("lec", dirname, "reading.html")
        if os.path.exists(reading):
            meta += f'\n<b>Read</b>: <a href="{reading}">Course Notes</a> (<a href="{reading.replace(".html", ".ipynb")}">NB</a>)<br>'
        meta = re.sub("^(https://mediaspace.wisc.edu.*)$",
                      r'<b>Watch</b>: <a href="\g<1>">Lecture</a><br>',
                      meta, flags=re.MULTILINE)
        days.append(meta)
    return days

def schedule():
    days = read_days()

    f = open('schedule.content.html', 'w', encoding='utf-8')
    f.write('<h1 class="mt-5">Course Schedule</h1>\n')

    day_count = (END_DATE - START_DATE).days + 1

    with open('schedule.json') as extra_sched:
        extra = json.loads(extra_sched.read())
    sections = extra['sections'] # indexed by week
    holiday = extra['holiday']

    cells = []
    full = 0
    free = 0
    for curr in (START_DATE + timedelta(n) for n in range(day_count)):
        day = calendar.day_abbr[curr.weekday()]
        if day in ['Mon', 'Wed', 'Fri']:
            if len(days) == 0:
                free += 1
            else:
                full += 1

            dname = curr.strftime("%m/%d")
            if dname in holiday:
                content = "\n".join(holiday[dname]) + "\n"
            else:
                content = days.pop(0) if len(days)>0 else 'TBD\n'
                if CUTOFF_DATE != None and curr >= CUTOFF_DATE:
                    projects = re.findall(".*Released:.*", content)
                    content = "Not Posted Yet\n" + "\n".join(projects)
            title,content = content[:content.index('\n')], content[content.index('\n')+1:]
            header = '<h5><strong>%s, %s</strong><br>%s</h5>' % (curr.strftime("%a"),
                                                                 curr.strftime("%b %-d"),
                                                                 title)
            cells.append('%s\n%s\n' % (header, content))
    print('%d free days, %d full days' % (free, full))

    # dump cells
    cols = 3
    for i in range(0, len(cells), cols):
        week = i//cols+1

        # sections
        for section in sections.get(str(week), []):
            f.write('<div class="alert alert-primary my-5 week">%s</div>\n' % section)

        # days
        row = cells[i:i+cols]
        f.write('<h3 class="my-3 border-bottom border-top">Week %d</h2>\n' % week)

        f.write('<div class="row">\n')
        for day, cell in enumerate(row):
            f.write('<div class="col-md-4 my-3">\n')
            f.write(cell)

            # week/quiz
            if day == 1 and week in extra["quizzes"]:
                if week > 2:
                    f.write(f'<b>Quiz</b>: <a href="{canvas}/quizzes">week {week-1} and before (cumulative)</a>\n')
                else:
                    f.write(f'<b>Quiz</b>: <a href="{canvas}/quizzes">week {week-1}</a>\n')

            f.write('</div>\n')
        f.write('</div>\n')
    f.write('<br>')

    f.close()

def main():
    schedule()
    template()

if __name__ == '__main__':
    main()
