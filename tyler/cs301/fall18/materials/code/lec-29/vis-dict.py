import sys, json

# get the data
assert(len(sys.argv) == 2)
arg = sys.argv[1]
d = json.loads(arg)

# generate value pages
paths = []
for key in d:
    path = key + '.html'
    paths.append(path)
    print(path)
    f = open(path, "w")
    f.write(str(d[key]))
    f.close()

# generate key page
print(paths)
f = open("key.html", "w")
for path in paths:
    f.write('<a href="' + path + '">')
    f.write(path)
    f.write("</a>")
    f.write("<br>\n")
f.close()

