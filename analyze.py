import pandas as pd
import os

if not os.path.exists("data.csv"):
    print("no data yet")
    exit()

df = pd.read_csv("data.csv")

if df.empty:
    print("empty data")
    exit()

# ===== 時間處理 =====
df["time"] = pd.to_datetime(df["time"])
df["round"] = (df["time"].astype(int) // 10**9 // 300) * 300

results = []

for r, group in df.groupby("round"):
    record = {
        "round": r,
        "up_hit_10": (group["up"] <= 0.10).any(),
        "down_hit_10": (group["down"] <= 0.10).any(),
        "up_hit_30": (group["up"] <= 0.30).any(),
        "down_hit_30": (group["down"] <= 0.30).any(),
        "up_hit_80": (group["up"] >= 0.80).any(),
        "down_hit_80": (group["down"] >= 0.80).any(),
        "up_hit_95": (group["up"] >= 0.95).any(),
        "down_hit_95": (group["down"] >= 0.95).any(),
    }

    results.append(record)

result_df = pd.DataFrame(results)
result_df.to_csv("rounds.csv", index=False)

print("分析完成")
