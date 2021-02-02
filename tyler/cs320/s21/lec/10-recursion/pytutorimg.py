from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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

def viz_code(b, lines, outfile="demo.png", line=None, times=None, includecode=True):
    b.get("http://localhost:8003/live.html#mode=edit")
    time.sleep(0.5)
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
            time.sleep(0.2)
            while curr_line(b) != line:
                fwd.click()
            if i < times - 1:
                fwd.click()

    # find element to snapshot (either just stack+heap, or sometimes code too)
    if not includecode:
        element = b.find_element_by_id("pyOutputPane")
    else:
        for element in b.find_elements_by_tag_name("table"):
            try:
                b.find_element_by_id("pyOutputPane")
                break
            except NoSuchElementException:
                pass
        else:
            raise Exception("could not find <table> that contains a pyOutputPane element")

    #https://stackoverflow.com/questions/13832322/how-to-capture-the-screenshot-of-a-specific-element-rather-than-entire-page-usin
    location = element.location
    size = element.size
    b.save_screenshot("/tmp/screenshot.png")
    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h
    im = Image.open("/tmp/screenshot.png")
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(outfile)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pytutorimg.py <notebook> [filt]")
        return

    nb = sys.argv[1]
    filt = None if len(sys.argv) < 3 else sys.argv[2]

    with open(nb) as f:
        nb = json.load(f)

    b = None

    for cell in nb["cells"]:
        lines = cell["source"]
        if len(lines) == 0:
            continue
        if not lines[0].startswith("#"):
            continue
        parts = lines[0][1:].split(",")
        for part in parts:
            m = re.match(r"(.*\.png)\s*(\d+)?\s*(\d+)?\s*(\w+)?", part)
            if m:
                png, line, times, opts = m.group(1), m.group(2), m.group(3), m.group(4)
                if filt != None and not filt in png:
                    continue
                if line != None:
                    line = int(line)
                if times != None:
                    times = int(times)
                if opts == None:
                    opts = ""
                if b == None:
                    selopts = Options()
                    selopts.headless = headless
                    b = webdriver.Chrome(options=selopts)
                    b.set_window_size(1920, 1080)
                print(png)
                viz_code(b, lines, png, line, times,
                         includecode="c" in opts)

    if b != None:
        b.close()

if __name__ == "__main__":
    main()
