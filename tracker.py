import requests
import pandas as pd
from datetime import datetime
import os

FILE = "data.csv"

def fetch():
    try:
        res = requests.get("https://clob.polymarket.com/markets")
        data = res.json()

        # 👉 找 BTC 5m 市場
        btc_markets = [
            m for m in data
            if "btc" in m.get("question", "").lower()
            and "5m" in m.get("question", "").lower()
        ]

        if not btc_markets:
            return None, None, None

        # 👉 找最新（用 timestamp 最大）
        latest = sorted(
            btc_markets,
            key=lambda x: x.get("endDate", ""),
            reverse=True
        )[0]

        up = float(latest["outcomes"][0]["price"])
        down = float(latest["outcomes"][1]["price"])

        market_id = latest.get("conditionId")

        return up, down, market_id

    except Exception as e:
        print("fetch error:", e)
        return None, None, None


up, down, market_id = fetch()

row = {
    "time": datetime.utcnow(),
    "up": up if up is not None else -1,
    "down": down if down is not None else -1,
    "market": market_id
}

df = pd.DataFrame([row])

if os.path.exists(FILE):
    df.to_csv(FILE, mode='a', header=False, index=False)
else:
    df.to_csv(FILE, index=False)

print("saved:", row)
