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

    # ===== 95c 剩餘時間 =====
    group = group.sort_values("time")

    up_95 = group[group["up"] >= 0.95]
    if not up_95.empty:
        first = up_95.iloc[0]["time"]
        last = group.iloc[-1]["time"]
        record["up_95_time_left"] = (last - first).total_seconds()
    else:
        record["up_95_time_left"] = None

    down_95 = group[group["down"] >= 0.95]
    if not down_95.empty:
        first = down_95.iloc[0]["time"]
        last = group.iloc[-1]["time"]
        record["down_95_time_left"] = (last - first).total_seconds()
    else:
        record["down_95_time_left"] = None

    results.append(record)

rounds = pd.DataFrame(results)
rounds.to_csv("rounds.csv", index=False)

# =========================
# 🔥 36局統計
# =========================

if len(rounds) >= 36:
    last36 = rounds.tail(36)

    both_30 = (last36["up_hit_30"] & last36["down_hit_30"]).sum()
    both_80 = (last36["up_hit_80"] & last36["down_hit_80"]).sum()
    both_95 = (last36["up_hit_95"] & last36["down_hit_95"]).sum()

    up95_avg = last36["up_95_time_left"].dropna().mean()
    down95_avg = last36["down_95_time_left"].dropna().mean()

    report = f"""
BTC 5m 最近36局分析

30c雙邊: {both_30}/36 ({both_30/36:.2%})
80c雙邊: {both_80}/36 ({both_80/36:.2%})
95c雙邊: {both_95}/36 ({both_95/36:.2%})

UP 95 平均剩餘秒數: {up95_avg}
DOWN 95 平均剩餘秒數: {down95_avg}
"""

    with open("report.txt", "w") as f:
        f.write(report)

    print(report)

else:
    print("不足36局")
