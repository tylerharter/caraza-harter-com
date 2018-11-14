import sys

items = sys.argv[1:]

f = open("list.html", "w")

f.write("Items:\n")
f.write("<ul>\n")
for item in items:
    f.write("<li>" + item + "\n")
f.write("</ul>\n")

f.close()