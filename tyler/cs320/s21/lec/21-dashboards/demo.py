from flask import Flask, Response, request
import pandas as pd
from matplotlib import pyplot as plt
from io import BytesIO
import random

values = [1,2,3]
app = Flask(__name__)

@app.route("/home.html")
def f():
    return '<html><body><img src="a.svg"></body></html>'

@app.route("/a.svg")
def g():
    pass # code hidden

@app.route("/b.svg")
def h():
    pass # code hidden

app.run("0.0.0.0", debug=True)
