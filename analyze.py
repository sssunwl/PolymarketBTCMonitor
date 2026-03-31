import pandas as pd

df = pd.read_csv("data.csv")

# ===== 時間處理 =====
df["time"] = pd.to_datetime(df["time"])
df["round"] = (df["time"].astype(int) // 10**9 // 300) * 300

results = []

# ===== 分局分析 =====
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

    # ===== 95c 剩餘時間 =====
    group = group.sort_values("time")

    up_95 = group[group["up"] >= 0.95]
    if not up_95.empty:
        first_time = up_95.iloc[0]["time"]
        end_time = group.iloc[-1]["time"]
        record["up_95_time_left"] = (end_time - first_time).total_seconds()
    else:
        record["up_95_time_left"] = None

    down_95 = group[group["down"] >= 0.95]
    if not down_95.empty:
        first_time = down_95.iloc[0]["time"]
        end_time = group.iloc[-1]["time"]
        record["down_95_time_left"] = (end_time - first_time).total_seconds()
    else:
        record["down_95_time_left"] = None

    results.append(record)

result_df = pd.DataFrame(results)
result_df.to_csv("rounds.csv", index=False)

print("分析完成")
