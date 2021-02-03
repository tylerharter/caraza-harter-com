#!/usr/bin/python3
import os, sys, json, re
from subprocess import check_output

def main():
    src = sys.argv[1]
    dst = src.replace(".md", ".html")
    assert ".md" in src
    check_output(["grip", src, "--export", dst])

    with open(dst) as f:
        html = f.read()

    html = re.sub(r'<h3>\s+<span class="octicon octicon-book"></span>\s+.*.md\s+</h3>', '', html)
    with open(dst, "w") as f:
        f.write(html)

if __name__ == '__main__':
     main()
