routes = {}

def route(url):
    def wrap(fn):
        routes[url] = fn
        return fn
    return wrap

@route("/")
def home():
    print("home")

@route("/donate.html")
def page2():
    print("donate")

for resource in ["/", "/donate.html", "missing.html"]:
    fn = routes.get(resource)
    if fn == None:
        print("404!")
        continue
    fn()
