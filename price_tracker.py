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

# 👉 安全初始化
best_pair = None
best_diff = 999

# 👉 找最接近 1 的兩個值
for i in range(len(values)):
    for j in range(i + 1, len(values)):
        s = values[i] + values[j]
        diff = abs(s - 1)

        if diff < best_diff:
            best_diff = diff
            best_pair = (values[i], values[j])

# 👉 防止 crash（關鍵）
if best_pair is not None:
    up_price, down_price = best_pair
else:
    print("No valid pair found")
