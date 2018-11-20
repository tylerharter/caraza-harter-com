import sys, json

in_text = sys.argv[1]
d = json.loads(in_text)

paths = []

# step 1: generate value pages
for key in d:
    val = d[key]
    path = key + ".html"
    paths.append(path)
    f = open(path, "w")
    f.write(str(val))
    f.close()

# step 2: generate keys.html
f = open("keys.html", "w")
f.write("Keys:\n")
f.write("<ul>\n")

template = '<a href="{}">{}</a>'
for path in paths:
    hlink = template.format(path, path)
    f.write("<li>" + hlink + "<br>\n")

f.write("</ul>\n")
f.close()