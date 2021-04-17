from flask import Flask, request
import random, pickle
import pandas as pd

app = Flask("grocery")

ads = {
    "soda": '<a href="ad.html?user_id={user_id}&item=Soda&price=0.80">Tasty Soda</a>',
    "coffee": '<a href="ad.html?user_id={user_id}&item=Coffee&price=1.50">Electric Coffee</a>',
    "wine": '<a href="ad.html?user_id={user_id}&item=Wine&price=8.99">Zesty Wine</a>',
}

@app.route("/")
def home():
    return """
    <h1>Wisconsin Grocery Store Search</h1>
    Zip Code: <input id="zipcode">
    <button onclick="window.location.href='listing.html?user_id='+Math.floor(Math.random()*1000000)+'&zipcode='+document.getElementById('zipcode').value">Go!</button>
    """

@app.route("/listing.html")
def listing():
    user_id = request.args["user_id"]
    zipcode = request.args["zipcode"]

    # select ad
    ad_name = random.choice(list(ads.keys()))
    ad_text = ads[ad_name].format(user_id=user_id)

    # generate page
    return """
    <h1>Grocery Stores in {zipcode}</h1>

    <ul>
    <li>Store 1
    <li>Store 2
    <li>Store 3
    <li>TODO: real stores...
    </ul>

    <p><b>Special Offer</b>: {ad}</p>
    """.format(zipcode=zipcode, ad=ad_text)

@app.route("/ad.html")
def ad():
    user_id = request.args["user_id"]
    item = request.args["item"]
    price = request.args["price"]
    return f"<h1>{item}</h1> On sale for ${price}..."

app.run("0.0.0.0", debug=True)
