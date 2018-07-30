#!/usr/bin/env python
import calendar, os
from datetime import date, timedelta

def template():
    with open('template.html') as f:
        template = f.read()
    suffix = '.content.html'
    for path in os.listdir('.'):
        if path.endswith(suffix):
            with open(path) as f:
                content = f.read()
            new = path[:-len(suffix)] + '.html'
            print('%s => %s' % (path, new))
            with open(new, 'w') as f:
                full = template.replace("{CONTENT}", content)
                f.write(full)

def format_day(day):
    lines = day.split('\n')
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
    f.write('<h1 class="mt-5">Lecture Schedule</h1>\n')
    
    start_date = date(2018, 9, 3)
    end_date = date(2018, 12, 12)
    day_count = (end_date - start_date).days + 1

    cells = []
    free = 0
    for curr in (start_date + timedelta(n) for n in range(day_count)):
        day = calendar.day_abbr[curr.weekday()]
        if day in ['Mon', 'Wed', 'Fri']:
            if len(days) == 0:
                free += 1
            content = days.pop(0) if len(days)>0 else 'TBD\n...'
            title,content = content[:content.index('\n')], content[content.index('\n')+1:]
            header = '<h4>%s: %s (%s)</h4>' % (curr.strftime("%a"),
                                               title,
                                               curr.strftime("%b %-d"))
            cells.append('%s\n%s\n' % (header, content))
    print('%d free days' % free)

    # dump cells
    cols = 3
    for i in range(0, len(cells), cols):
        row = cells[i:i+cols]
        f.write('<div class="alert alert-primary my-4 week">Week %d</div>\n' % (i/cols+1))
        f.write('<div class="row">\n')
        for cell in row:
            f.write('<div class="col-md-4">\n')
            f.write(cell)
            f.write('</div>\n')
        f.write('</div>\n')
    f.write('<br>')

    f.close()

def main():
    schedule()
    template()

if __name__ == '__main__':
    main()
