import requests
import pandas as pd
from datetime import datetime
import os

FILE = "data.csv"

def fetch():
    try:
        res = requests.get("https://clob.polymarket.com/markets")
        data = res.json()

        if not data or len(data) == 0:
            return None, None

        # 👉 找第一個有價格的市場（避免空資料）
        for m in data:
            try:
                up = float(m["outcomes"][0]["price"])
                down = float(m["outcomes"][1]["price"])
                return up, down
            except:
                continue

        return None, None

    except Exception as e:
        print("fetch error:", e)
        return None, None

up, down = fetch()

# 👉 就算抓不到，也寫一筆（關鍵）
row = {
    "time": datetime.utcnow(),
    "up": up if up is not None else -1,
    "down": down if down is not None else -1
}

df = pd.DataFrame([row])

# 👉 強制寫入
if os.path.exists(FILE):
    df.to_csv(FILE, mode='a', header=False, index=False)
else:
    df.to_csv(FILE, index=False)

print("saved:", row)
