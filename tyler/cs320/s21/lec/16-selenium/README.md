# Web Scraping

For web scraping, we'll learn a tool called selenium, which lets our
Python code take control of an actual web browser.  This is more
powerful than the `requests` module taught in 220, as we can do things
like type text and automate clicks.

Selenium is tricky to install (it requires three parts that must be
compatible: pip package, browser, and driver).  In the first video,
I'll explain how to find the right versions of these.  For your
convenience, though, here's a series of a commands that we've tested
that perform installs of all three pieces:

```
pip3 install selenium
sudo apt -y install unzip htop chromium-browser
rm -f chromedriver_linux64.zip
wget https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver ~/.local/bin
```

When it's all done, run both of the following, and verify that both
versions start with 87 (like "87.X.X.X"):

```
chromium-browser --version
chromedriver --version
```

**Note 1**: your virtual machine does not have a graphical user interface,
so you won't be able to follow some of the early examples until I show
how to run in "headless" mode (unrelated to git's headless) and take
screenshots, unless you figure out how to install selenium on your
laptop as well for fun (we don't require it, as it can often get quite
tricky except on the VMs).

**Note 2**: launching many web browsers via code can quickly eat up
  all the memory on your VM.  You can run the `htop` command to see
  how much memory you have (hit "q" to quit when done).  If you're low
  on memory (you might notice your VM being sluggish), you can run
  `pkill chromium` shutdown all browser instances hanging around in
  the background.

## 1. Requests vs. Selenium

### Watch: [18-minute video](https://youtu.be/0qgdQejk3LM)

## 2. Selenium Example: Slow Table

### Watch: [24-minute video](https://youtu.be/RzNBu_Pu3HM)

### Practice: Screenshot

In a notebook on your virtual machine, create a headless browser
instance:

```python
from IPython.core.display import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

options = Options()
options.headless = True
b = webdriver.Chrome(options=options)
```

Navigate the browser to the URL of your favorite website, and save a screenshot:

```python
b.get("????")
b.save_screenshot("screenshot.png")
```

View the screenshot in the notebook:

```python
Image("screenshot.png")
```

## 3. Selenium Example: Load More

### Watch: [7-minute video](https://youtu.be/xaVUIp5gIc0)
