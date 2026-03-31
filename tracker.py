import time
import pandas as pd
from datetime import datetime
import os

FILE = "data.csv"

# ===== 每5分鐘一局 =====
def get_round():
    now = int(time.time())
    return (now // 300) * 300

# ===== 對應 URL =====
def get_url(round_id):
    return f"https://polymarket.com/event/btc-updown-5m-{round_id}"

round_id = get_round()
url = get_url(round_id)

row = {
    "time": datetime.utcnow(),
    "round": round_id,
    "url": url
}

df = pd.DataFrame([row])

if os.path.exists(FILE):
    df.to_csv(FILE, mode='a', header=False, index=False)
else:
    df.to_csv(FILE, index=False)

print("saved:", row)
