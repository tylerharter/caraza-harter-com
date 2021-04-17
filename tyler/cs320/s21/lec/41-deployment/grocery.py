from flask import Flask, request
import random, pickle
import pandas as pd

app = Flask("grocery")

log_file = open("train.txt", "w")

incomes = pd.read_csv("income.csv").set_index("zip")

with open("models.pkl", "rb") as f:
    models = pickle.load(f)

ads = {
    "soda": '<a href="ad.html?user_id={user_id}&item=Soda&price=0.80">Tasty Soda</a>',
    "coffee": '<a href="ad.html?user_id={user_id}&item=Coffee&price=1.50">Electric Coffee</a>',
    "wine": '<a href="ad.html?user_id={user_id}&item=Wine&price=8.99">Zesty Wine</a>',
}

def click_prob(zipcode, ad_name):
    return models[ad_name].predict_proba(incomes.loc[[zipcode]])[0,1]

def get_best_ad(zipcode):
    best_prob = 0
    for ad_name in ads.keys():
        prob = click_prob(zipcode, ad_name)
        if prob > best_prob:
            best_prob = prob
            best_ad = ad_name
    return best_ad

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
    #ad_name = random.choice(list(ads.keys()))
    ad_name = get_best_ad(int(zipcode))
    ad_text = ads[ad_name].format(user_id=user_id)
    
    log_file.write(f"SHOW {user_id} {zipcode} {ad_name}\n")
    log_file.flush() # any written data in Python's memory should go out

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
    
    log_file.write(f"CLICK {user_id}\n")
    log_file.flush()
    
    return f"<h1>{item}</h1> On sale for ${price}..."

app.run("0.0.0.0", debug=True)
