import os, sys, json
import pandas as pd
from flask import Flask
from graphviz import Graph

app = Flask(__name__)

@app.route("/rand.svg")
def rand_plot():
    g = Graph()
    g.edge("a", "b")
    g.edge("b", "c")
    g.edge("c", "a")
    return g._repr_svg_()

if __name__ == '__main__':
    app.run("0.0.0.0", "54321")
