import time
from datetime import datetime
import csv
import os

FILE = "data.csv"

now = int(time.time())
round_id = (now // 300) * 300

row = [str(datetime.utcnow()), round_id]

# 寫入 CSV（最穩方式，不用 pandas）
file_exists = os.path.isfile(FILE)

with open(FILE, "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["time", "round"])
    writer.writerow(row)

print("saved:", row)
