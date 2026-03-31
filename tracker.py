import time
import requests
import pandas as pd
from datetime import datetime

ROUND_SECONDS = 300

def new_round():
    return {
        "start_time": datetime.now(),
        "up_hit_10": False,
        "down_hit_10": False,
        "up_hit_30": False,
        "down_hit_30": False,
        "up_hit_80": False,
        "down_hit_80": False,
        "up_hit_95": False,
        "down_hit_95": False,
        "up_95_time_left": None,
        "down_95_time_left": None
    }

current = new_round()
round_start = time.time()

def fetch_price():
    try:
        res = requests.get("https://clob.polymarket.com/markets")
        data = res.json()[0]

        up = float(data["outcomes"][0]["price"])
        down = float(data["outcomes"][1]["price"])

        return up, down
    except:
        return None, None

def update(up, down):
    elapsed = time.time() - round_start
    time_left = int(ROUND_SECONDS - elapsed)

    if up <= 0.10: current["up_hit_10"] = True
    if down <= 0.10: current["down_hit_10"] = True

    if up <= 0.30: current["up_hit_30"] = True
    if down <= 0.30: current["down_hit_30"] = True

    if up >= 0.80: current["up_hit_80"] = True
    if down >= 0.80: current["down_hit_80"] = True

    if up >= 0.95 and not current["up_hit_95"]:
        current["up_hit_95"] = True
        current["up_95_time_left"] = time_left

    if down >= 0.95 and not current["down_hit_95"]:
        current["down_hit_95"] = True
        current["down_95_time_left"] = time_left

def save():
    df = pd.DataFrame([current])
    df.to_csv("PolymarketBTCMonitor.csv",
              mode='a',
              header=not pd.io.common.file_exists("PolymarketBTCMonitor.csv"),
              index=False)

print("🚀 開始監測")

while True:
    up, down = fetch_price()

    if up and down:
        print(up, down)
        update(up, down)

    if time.time() - round_start >= ROUND_SECONDS:
        save()
        print("✅ 已記錄一局")

        current = new_round()
        round_start = time.time()

    time.sleep(1)
