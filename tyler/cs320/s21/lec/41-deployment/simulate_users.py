import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup

def main():
    if not len(sys.argv) == 2:
        print("Usage: simulate_users.py <visit file>")
        return

    visits = pd.read_csv(sys.argv[1])
    clicks = 0

    baseurl = "http://localhost:5000/"
    for row in visits.itertuples():
        url = baseurl + f"listing.html?user_id={row.Index}&zipcode={row.zip}"
        print(url)
        r = requests.get(url)
        r.raise_for_status()

        # should we click an ad?
        doc = BeautifulSoup(r.text, "html.parser")
        for link in doc.find_all("a"):
            click = False
            if row.soda and "soda" in link.text.lower():
                click = True
            elif row.coffee and "coffee" in link.text.lower():
                click = True
            elif row.wine and "wine" in link.text.lower():
                click = True
            if click == True:
                print("CLICK " + link.attrs["href"])
                clicks += 1
                r = requests.get(baseurl + link.attrs["href"])
                r.raise_for_status()
                break

    print(f"Click rate: {100 * clicks / len(visits)}")

if __name__ == '__main__':
     main()
