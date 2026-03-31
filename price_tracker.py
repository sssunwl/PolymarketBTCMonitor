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

# 👉 找最接近互補的一組（核心）
best_pair = None
best_diff = 999

for i in range(len(values)):
    for j in range(i + 1, len(values)):
        s = values[i] + values[j]
        diff = abs(s - 1)

        if diff < best_diff:
            best_diff = diff
            best_pair = (values[i], values[j])

if best_pair:
    up_price, down_price = best_pair
