import pandas as pd
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()
        print("BEFORE:", html)
        html = html.format(time.time())
        print("AFTER:", html)

    return html

@app.route('/ha.html')
def ha_page():
    mult = int(request.args.get("mult"))
    print(mult, type(mult))
    return "ha " * mult

if __name__ == '__main__':
    app.run(host="0.0.0.0") # don't change this line!