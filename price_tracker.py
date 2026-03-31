import time
from datetime import datetime
import csv
import os

FILE = "price.csv"

def get_round():
    now = int(time.time())
    return (now // 300) * 300

def get_url(round_id):
    return f"https://polymarket.com/event/btc-updown-5m-{round_id}"

round_id = get_round()
url = get_url(round_id)

up_price = -1
down_price = -1

try:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_timeout(8000)

        elements = page.locator("text=¢")
        texts = elements.all_inner_texts()

        values = []

        for t in texts:
            try:
                if "¢" in t:
                    val = float(t.replace("¢", "").strip()) / 100
                    if 0 <= val <= 1:
                        values.append(val)
            except:
                continue

        print("RAW:", values)

        if len(values) >= 2:
            up_price = values[0]
            down_price = values[1]

        browser.close()

except Exception as e:
    print("ERROR:", e)

# ===== 永遠寫入 =====
file_exists = os.path.isfile(FILE)

with open(FILE, "a", newline="") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(["time", "round", "up", "down"])

    writer.writerow([str(datetime.utcnow()), round_id, up_price, down_price])

print("saved:", up_price, down_price)
