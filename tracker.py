import requests
import pandas as pd
from datetime import datetime
import os

FILE = "data.csv"

def fetch():
    try:
        res = requests.get("https://clob.polymarket.com/markets")
        data = res.json()[0]

        up = float(data["outcomes"][0]["price"])
        down = float(data["outcomes"][1]["price"])

        return up, down
    except Exception as e:
        print("fetch error:", e)
        return None, None

up, down = fetch()

if up is None or down is None:
    print("no data")
    exit()

row = {
    "time": datetime.utcnow(),
    "up": up,
    "down": down
}

df = pd.DataFrame([row])

if os.path.exists(FILE):
    df.to_csv(FILE, mode='a', header=False, index=False)
else:
    df.to_csv(FILE, index=False)

print("saved:", row)
