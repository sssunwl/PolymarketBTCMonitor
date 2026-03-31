import time
import pandas as pd
from datetime import datetime, timezone, timedelta
import os

FILE = "data.csv"

# ===== 轉 ET 時間 =====
def get_et_timestamp():
    utc_now = datetime.now(timezone.utc)
    et_now = utc_now - timedelta(hours=4)  # EST (簡化版，夠用)
    return int(et_now.timestamp())

# ===== 算 round =====
def get_round():
    et_ts = get_et_timestamp()
    return (et_ts // 300) * 300

# ===== URL =====
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
