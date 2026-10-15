
import json
from pathlib import Path
from collections import Counter

JSON_PATH = Path(
    "D:/bdd100k/bdd100k_labels_release/labels/bdd100k_labels_images_train.json"
)

TARGET_CLASSES = {"person", "car", "traffic light"}

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

night_total = 0
night_with_targets = 0
night_without_targets = 0

target_counts = Counter()
night_class_counts = Counter()

for item in data:
    attributes = item.get("attributes", {})

    if attributes.get("timeofday") != "night":
        continue

    night_total += 1

    # Chỉ giữ đối tượng thuộc ba lớp mục tiêu
    targets = [
        label for label in item.get("labels", [])
        if label.get("category") in TARGET_CLASSES
        and isinstance(label.get("box2d"), dict)
        and all(
            key in label["box2d"]
            for key in ("x1", "y1", "x2", "y2")
        )
    ]

    classes_in_image = {label["category"] for label in targets}
    target_counts.update(classes_in_image)
    night_class_counts.update(label["category"] for label in targets)

    if targets:
        night_with_targets += 1
    else:
        night_without_targets += 1

print("=== THONG KE ANH BAN DEM ===")
print("Tong anh night trong JSON:", night_total)
print("Anh night co lop muc tieu:", night_with_targets)
print("Anh night khong co lop muc tieu:", night_without_targets)

print("\n=== SO ANH CO TUNG LOP ===")
for cls in sorted(TARGET_CLASSES):
    print(f"{cls}: {target_counts[cls]:,} anh")

print("\n=== SO BOUNDING BOX THEO LOP ===")
for cls in sorted(TARGET_CLASSES):
    print(f"{cls}: {night_class_counts[cls]:,} bounding boxes")
