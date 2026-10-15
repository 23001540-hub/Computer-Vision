
import json
from pathlib import Path
from collections import Counter

JSON_PATH = Path(
    "D:/bdd100k/bdd100k_labels_release/labels/bdd100k_labels_images_train.json"
)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Đếm số ảnh theo thời điểm trong ngày
counter = Counter()

for item in data:
    timeofday = item.get("attributes", {}).get(
        "timeofday", "unknown"
    )
    counter[timeofday] += 1

print("TONG SO ANH:", len(data))
print("\nTHONG KE THEO THOI DIEM:")

for name, count in counter.most_common():
    percentage = count / len(data) * 100
    print(f"{name:15s}: {count:6,d} anh ({percentage:.2f}%)")

# Đếm riêng ảnh ban đêm
night_count = counter.get("night", 0)

print("\nSO ANH BAN DEM:", night_count)
if len(data) > 0:
    print(f"TY LE ANH BAN DEM: {night_count / len(data) * 100:.2f}%")
