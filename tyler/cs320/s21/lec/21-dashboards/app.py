from flask import Flask, Response
from matplotlib import pyplot as plt
from io import BytesIO
import pandas as pd
import random

plt.switch_backend('agg')
app = Flask(__name__)
values = [1,2,5,4,8,7,3,3,4,2,3]

@app.route("/")
def home():
    values.append(random.randint(1, 10))
    
    html = """
    <html>
    <body>
    <h1>Values over Time</h1>
    <img src="val_over_time.svg">

    <h1>CDF</h1>
    <img src="cdf.svg">

    <h1>Sorted Values</h1>
    <img src="sorted.svg">
    </body>
    </html>
    """

    return html

@app.route("/cdf.svg")
def cdf():
    fig, ax = plt.subplots()
    s = pd.Series(sorted(values))
    rev = pd.Series(100*(s.index+1)/len(s), index=s.values)
    rev.plot.line(ax=ax)
    ax.set_xlabel("Values")
    ax.set_ylabel("Percent Less")

    buf = BytesIO()
    fig.savefig(buf)
    return Response(buf.getvalue(), headers={"Content-Type": "image/xml+svg"})

@app.route("/sorted.svg")
def sorted_values():
    fig, ax = plt.subplots()
    pd.Series(sorted(values)).plot.line(ax=ax)

    buf = BytesIO()
    fig.savefig(buf)
    return Response(buf.getvalue(), headers={"Content-Type": "image/xml+svg"})

@app.route("/val_over_time.svg")
def over_time():
    fig, ax = plt.subplots()
    pd.Series(values).plot.line(ax=ax)

    buf = BytesIO()
    fig.savefig(buf)
    return Response(buf.getvalue(), headers={"Content-Type": "image/xml+svg"})

if __name__ == '__main__':
     app.run("0.0.0.0", debug=True)
