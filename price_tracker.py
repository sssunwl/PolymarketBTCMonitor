import time
from datetime import datetime
import csv
import os

from playwright.sync_api import sync_playwright

FILE = "price.csv"

def get_round():
    now = int(time.time())
    return (now // 300) * 300

def get_url(round_id):
    return f"https://polymarket.com/event/btc-updown-5m-{round_id}"

round_id = get_round()
url = get_url(round_id)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(url, timeout=60000)

    # 等畫面載入
    page.wait_for_timeout(5000)

    try:
        # 👉 抓按鈕（這裡是關鍵，可能會微調）
        buttons = page.locator("button")

        texts = buttons.all_inner_texts()

        up_price = None
        down_price = None

        for t in texts:
            if "%" in t:
                val = float(t.replace("%", "")) / 100
                if up_price is None:
                    up_price = val
                else:
                    down_price = val
                    break

        print("UP:", up_price, "DOWN:", down_price)

    except Exception as e:
        print("error:", e)
        up_price = -1
        down_price = -1

    browser.close()

# ===== 寫入 CSV =====
file_exists = os.path.isfile(FILE)

with open(FILE, "a", newline="") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(["time", "round", "up", "down"])

    writer.writerow([str(datetime.utcnow()), round_id, up_price, down_price])
