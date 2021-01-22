from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import Image
import pyperclip
from IPython.core.display import display, HTML, Image as IPythonImage
import pandas as pd
import time, sys, json, re

headless = True

def curr_line(b):
    for i, el in enumerate(b.find_elements_by_class_name("ace_gutter-cell")):
        classes = el.get_attribute("class").split()
        if "curLineStepGutter" in classes or "curPrevOverlapLineStepGutter" in classes:
            return i + 1
    raise Exception("line unreachable")

def viz_code(lines, outfile="demo.png", line=None, times=None):
    opts = Options()
    opts.headless = headless
    b = webdriver.Chrome(options=opts)
    b.set_window_size(1920, 1080)
    b.get("http://localhost:8003/live.html#mode=edit")
    txt = b.find_element_by_tag_name("textarea")

    #txt.send_keys()
    pyperclip.copy("".join(lines))
    txt.send_keys(Keys.SHIFT, Keys.INSERT) # TODO: paste is different on Windows

    time.sleep(0.5)

    first = b.find_element_by_id("jmpFirstInstr")
    fwd = b.find_element_by_id("jmpStepFwd")
    last = b.find_element_by_id("jmpLastInstr")

    first.click()
    if line == None:
        last.click()
    else:
        if times == None:
            times = 1
        for i in range(times):
            while curr_line(b) != line:
                fwd.click()
            if i < times - 1:
                fwd.click()

    #https://stackoverflow.com/questions/13832322/how-to-capture-the-screenshot-of-a-specific-element-rather-than-entire-page-usin
    element = b.find_element_by_id("pyOutputPane")
    location = element.location
    size = element.size
    b.save_screenshot(outfile)
    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h
    im = Image.open(outfile)
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(outfile)
    b.close()

def main2():
    if len(sys.argv) != 4:
        print("Usage: python3 pytutorimg.py <notebook> <cell> <img>")
        return

    nb, cell, outpng = sys.argv[1:]

    with open(nb) as f:
        nb = json.load(f)

    cell = [c for c in nb["cells"] if c["execution_count"] == int(cell)][0]
    print(cell)
    lines = cell["source"]

    viz_code(lines, outpng)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 pytutorimg.py <notebook>")
        return

    nb = sys.argv[1]

    with open(nb) as f:
        nb = json.load(f)

    for cell in nb["cells"]:
        lines = cell["source"]
        if len(lines) == 0:
            continue
        m = re.match(r"\#\s*(.*\.png)\s*(\d+)?\s*(\d+)?", lines[0])
        if m:
            png, line, times = m.group(1), m.group(2), m.group(3)
            if line != None:
                line = int(line)
            if times != None:
                times = int(times)
            if png != "constructor.png":
                continue
            viz_code(lines, png, line, times)

if __name__ == "__main__":
    main()
