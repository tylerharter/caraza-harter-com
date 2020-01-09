#!/usr/bin/env python
import calendar, os, json
from datetime import date, timedelta

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

def format_day(day):
    lines = list(filter(lambda line: not line.startswith('#'), day.split('\n')))
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
    return '\n'.join(out)

def schedule():
    with open('schedule.txt') as f:
        days = list(map(format_day, f.read().split('=\n')))

    f = open('schedule.content.html', 'w', encoding='utf-8')
    f.write('<h1 class="mt-5">Course Schedule</h1>\n')

    start_date = date(2020, 1, 20)
    end_date = date(2020, 5, 1)
    day_count = (end_date - start_date).days + 1

    cells = []
    full = 0
    free = 0
    for curr in (start_date + timedelta(n) for n in range(day_count)):
        day = calendar.day_abbr[curr.weekday()]
        if day in ['Mon', 'Wed', 'Fri']:
            if len(days) == 0:
                free += 1
            else:
                full += 1
            content = days.pop(0) if len(days)>0 else 'TBD\n...'
            title,content = content[:content.index('\n')], content[content.index('\n')+1:]
            header = '<h5><strong>[%s]</strong> %s (%s)</h5>' % (curr.strftime("%a"),
                                               title,
                                               curr.strftime("%b %-d"))
            cells.append('%s\n%s\n' % (header, content))
    print('%d free days, %d full days' % (free, full))

    with open('schedule.json') as extra_sched:
        extra = json.loads(extra_sched.read())
    events = extra['events'] # indexed by week
    sections = extra['sections'] # indexed by week
    
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
        for cell in row:
            f.write('<div class="col-md-4 my-3">\n')
            f.write(cell)
            f.write('</div>\n')
        f.write('</div>\n')

        # warnings
        for event in events.get(str(week), []):
            f.write('<div class="alert alert-danger my-2">%s</div>\n' % event)
    f.write('<br>')

    f.close()

def main():
    schedule()
    template()

if __name__ == '__main__':
    main()
