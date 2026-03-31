# 等畫面載入
page.wait_for_timeout(8000)

up_price = None
down_price = None

try:
    # 👉 抓所有含 ¢ 的文字
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

    # 👉 前兩個就是 Up / Down
    if len(values) >= 2:
        up_price = values[0]
        down_price = values[1]

except Exception as e:
    print("error:", e)

print("UP:", up_price, "DOWN:", down_price)
