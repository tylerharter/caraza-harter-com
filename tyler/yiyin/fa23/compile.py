#!/usr/bin/env python3
import calendar, os, json, re
from datetime import date, timedelta
import json

github = 'https://github.com/tylerharter/caraza-harter-com/blob/master/tyler/yiyin/su23'
canvas = 'https://canvas.wisc.edu/courses/355770'
lab_project_github = 'https://github.com/yiyins2/CS320-SU23/tree/main'

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

def read_days():
    days = []
    for dirname in sorted(os.listdir("lec")):
        m = re.match(r"(\d\d)\-", dirname)
        if not m:
            continue
        num = m.group(1)
        meta = os.path.join("lec", dirname, "meta.json")
        with open(meta) as f:
            meta_dict = json.load(f)

        out = []
        #title 
        out.append(f'<span id="lec-{num}-title">{meta_dict["title"]}</span>')
        #topics
        if "topics" in meta_dict: 
            out.append('<ul class="compact-ul">')
            for i in meta_dict["topics"]: 
                out.append('<li>'+i)
            out.append('</ul>')

        #exam
        if "exam" in meta_dict:
            if "Midterm 1" == meta_dict["exam"]:
                out.append(f'\n<a href="{canvas}/quizzes" class="btn btn-primary btn-sm my-1 exam"><strong>Midterm 1</strong><br>Fri, June 30th, 7:00PM - 8:30PM</a><br>')
            elif "Midterm 2" == meta_dict["exam"]:
                out.append(f'\n<a href="{canvas}/quizzes" class="btn btn-primary btn-sm my-1 exam"><strong>Midterm 2</strong><br>Fri, July 21st, 7:00PM - 8:30PM</a><br>')

        #project
        if 'release' in meta_dict: 
            out.append(f'\n<a href="{lab_project_github}/{meta_dict["release"]}" class="btn btn-primary btn-sm my-1 release">{meta_dict["release"].upper()} Released</a><br>')
        if 'project' in meta_dict: 
            if meta_dict["project"] == "p3": 
                out.append(f'\n<a href="{lab_project_github}/{meta_dict["project"]}" class="btn btn-primary btn-sm my-1 project">{meta_dict["project"].upper()} Due <strong>Fri, July 7th</strong></a><br>')
            else: 
                out.append(f'\n<a href="{lab_project_github}/{meta_dict["project"]}" class="btn btn-primary btn-sm my-1 project">{meta_dict["project"].upper()} Due</a><br>')
        
        #slides
        slides = os.path.join("lec", dirname, "slides.pdf")
        if os.path.exists(slides):
            out.append(f'\n<a href="{slides}" class="btn btn-primary btn-sm my-1 slides">Slides</a><br>')
        
        #worksheet
        worksheet = os.path.join("lec", dirname, "worksheet.pdf")
        if os.path.exists(worksheet):
            answer = os.path.join("lec", dirname, "worksheet_answer.pdf")
            if os.path.exists(answer):
                out.append(f'\n<a href="{worksheet}" class="btn btn-primary btn-sm my-1 worksheet">Worksheet</a> <a href="{answer}" class="btn btn-primary btn-sm my-1 worksheet">Answer</a><br>')
            else:
                out.append(f'\n<a href="{worksheet}" class="btn btn-primary btn-sm my-1 worksheet">Worksheet</a><br>')
        
        #lec recording
        if 'watch' in meta_dict: 
            out.append(f'\n<a href="{meta_dict["watch"]}" class="btn btn-primary btn-sm my-1 watch">Lec Recording</a><br>')

        #reading
        reading = os.path.join("lec", dirname, "reading.md")
        if os.path.exists(reading):
            out.append(f'\n<a href="{github}/{reading}" class="btn btn-primary btn-sm my-1 read">Reading</a><br>')
        reading = os.path.join("lec", dirname, "reading.html")
        if os.path.exists(reading):
            out.append(f'\n<a href="{reading}" class="btn btn-primary btn-sm my-1 read">Reading</a> <a href="{reading.replace(".html", ".ipynb")}" class="btn btn-primary btn-sm my-1 read">.nb</a><br>')

        days.append('\n'.join(out))
    return days

def schedule():
    days = read_days()

    f = open('schedule.content.html', 'w', encoding='utf-8')
    f.write('<h1 class="mt-5">Course Schedule</h1>\n')

    start_date = date(2023, 6, 5)
    end_date = date(2023, 8, 10)
    day_count = (end_date - start_date).days + 1

    with open('schedule.json') as extra_sched:
        extra = json.loads(extra_sched.read())
    sections = extra['sections'] # indexed by week
    holiday = extra['holiday']

    cells = []
    full = 0
    free = 0
    for curr in (start_date + timedelta(n) for n in range(day_count)):
        day = calendar.day_abbr[curr.weekday()]
        if day in ['Mon', 'Tue', 'Wed', "Thu"]:
            if len(days) == 0:
                free += 1
            else:
                full += 1

            dname = curr.strftime("%m/%d")
            if dname in holiday:
                content = "\n".join(holiday[dname]) + "\n"
                if "Final" == holiday[dname][0]:
                    content += f'<a href="{canvas}/quizzes" class="btn btn-primary btn-sm my-1 exam"><strong>Final</strong><br>Thu, Aug 10th, 10:00AM - 12:30PM</a><br>\n'
            else:
                content = days.pop(0) if len(days)>0 else 'TBD\n...'
            title,content = content[:content.index('\n')], content[content.index('\n')+1:]
            header = '<h5>[%s, %s] <br> %s</h5>' % (curr.strftime("%a"),
                                               curr.strftime("%b %-d"), title)
            cells.append('%s\n%s\n' % (header, content))
    print('%d free days, %d full days' % (free, full))

    # dump cells
    cols = 4
    for i in range(0, len(cells), cols):
        week = i // cols + 1

        # sections
        for section in sections.get(str(week), []):
            f.write('<div class="alert alert-primary my-5 week">%s</div>\n' % section)

        # days
        row = cells[i:i+cols]
        f.write('<h3 class="my-3 border-bottom border-top">Week %d</h2>\n' % week)

        f.write('<div class="row">\n')
        for day, cell in enumerate(row):
            f.write('<div class="col-md-3 my-3">\n')
            f.write(cell)

            # lab 
            if day == 1 and week != 5: 
                f.write(f'<a href="{lab_project_github}/labs/lab{week}A.md" class="btn btn-primary btn-sm my-1 lab">Lab {week}A</a><br>\n')
            if day == 3 and week != 10: 
                f.write(f'<a href="{lab_project_github}/labs/lab{week}B.md" class="btn btn-primary btn-sm my-1 lab">Lab {week}B</a><br>\n')

            # quiz 
            if day == 3 and week in extra["labs"]:
                f.write(f'<a href="{canvas}/quizzes" class="btn btn-primary btn-sm my-1 quiz">Quiz {week}</a><br>\n')

            f.write('</div>\n')
        f.write('</div>\n')
    f.write('<br>')

    f.close()

def main():
    # schedule()
    template()

if __name__ == '__main__':
    main()
