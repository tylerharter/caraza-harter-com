#!/usr/bin/env python
import os

def main():
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

if __name__ == '__main__':
    main()
