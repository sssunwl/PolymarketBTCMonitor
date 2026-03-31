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

# ===== 分局 =====
rounds = df.groupby("round").size().reset_index(name="count")

rounds.to_csv("rounds.csv", index=False)

print("rounds updated:", len(rounds))

# ===== 測試用 report（先簡單）=====
if len(rounds) >= 5:
    last5 = rounds.tail(5)

    report = f"""
最近5局統計

局數: {len(last5)}

rounds:
{last5["round"].tolist()}
"""

    with open("report.txt", "w") as f:
        f.write(report)

    print(report)
else:
    print("不足5局")
