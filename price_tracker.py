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

# ===== 閾值 =====
up_10 = down_10 = 0
up_30 = down_30 = 0
up_80 = down_80 = 0
up_95 = down_95 = 0

try:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)

        # ===== 🔥 關鍵：等更久 + 模擬互動 =====
        page.wait_for_timeout(12000)
        page.mouse.click(1000, 200)   # 觸發 Live
        page.wait_for_timeout(3000)

        # ===== 抓右側 Buy 區 =====
        panel = page.locator("text=Buy").locator("..")
        texts = panel.locator("text=¢").all_inner_texts()

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

# ===== 判斷函數 =====
def check(val, threshold, mode):
    if val == -1:
        return 0
    if mode == "le":
        return 1 if val <= threshold else 0
    if mode == "ge":
        return 1 if val >= threshold else 0

# ===== 條件 =====
up_10 = check(up_price, 0.10, "le")
down_10 = check(down_price, 0.10, "le")

up_30 = check(up_price, 0.30, "le")
down_30 = check(down_price, 0.30, "le")

up_80 = check(up_price, 0.80, "ge")
down_80 = check(down_price, 0.80, "ge")

up_95 = check(up_price, 0.95, "ge")
down_95 = check(down_price, 0.95, "ge")

# ===== 寫入 CSV =====
file_exists = os.path.isfile(FILE)

with open(FILE, "a", newline="") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow([
            "time", "round", "up", "down",
            "up_10", "down_10",
            "up_30", "down_30",
            "up_80", "down_80",
            "up_95", "down_95"
        ])

    writer.writerow([
        str(datetime.utcnow()), round_id, up_price, down_price,
        up_10, down_10,
        up_30, down_30,
        up_80, down_80,
        up_95, down_95
    ])

print("UP:", up_price, "DOWN:", down_price)
print("10c:", up_10, down_10)
print("30c:", up_30, down_30)
print("80c:", up_80, down_80)
print("95c:", up_95, down_95)
