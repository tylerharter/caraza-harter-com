import sys
items = sys.argv[1:]
print(items)

f = open("list.html", "w")

f.write("<ul>\n")
for item in items:
    f.write("<li>" + item + "</li>\n")
f.write("</ul>\n")

f.close()