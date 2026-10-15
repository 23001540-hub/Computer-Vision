
import json
import shutil
from pathlib import Path
from collections import Counter

# ===== 1. DUONG DAN =====
JSON_PATH = Path(
    "D:/bdd100k/bdd100k_labels_release/labels/bdd100k_labels_images_train.json"
)

IMAGE_ROOT = Path("D:/bdd100k/bdd100k/images/100k/train")

OUTPUT_ROOT = Path("D:/bdd100k/night_dataset")
OUTPUT_IMAGES = OUTPUT_ROOT / "images"
OUTPUT_JSON = OUTPUT_ROOT / "labels_night.json"

TARGET_CLASSES = {"person", "car", "traffic light"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png"}

# ===== 2. DOC JSON =====
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

OUTPUT_IMAGES.mkdir(parents=True, exist_ok=True)

filtered_records = []
class_counts = Counter()
missing_images = []
copied_count = 0

# Lập chỉ mục tên ảnh -> đường dẫn thực tế
image_index = {}
for path in IMAGE_ROOT.rglob("*"):
    if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
        image_index.setdefault(path.name, path)

# ===== 3. LOC ANH VA NHAN =====
for item in data:
    if item.get("attributes", {}).get("timeofday") != "night":
        continue

    filtered_labels = []

    for label in item.get("labels", []):
        if label.get("category") not in TARGET_CLASSES:
            continue

        box = label.get("box2d")
        if not isinstance(box, dict):
            continue

        if not all(k in box for k in ("x1", "y1", "x2", "y2")):
            continue

        try:
            x1, y1 = float(box["x1"]), float(box["y1"])
            x2, y2 = float(box["x2"]), float(box["y2"])
        except (TypeError, ValueError):
            continue

        # Kiểm tra tọa độ và kích thước hộp
        if not (x2 > x1 and y2 > y1):
            continue

        filtered_labels.append(label)

    # Chỉ giữ ảnh có ít nhất một nhãn mục tiêu hợp lệ
    if not filtered_labels:
        continue

    name = item.get("name")
    source = image_index.get(name)

    if source is None:
        missing_images.append(name)
        continue

    # Sao chép ảnh, không thay đổi file gốc
    destination = OUTPUT_IMAGES / name
    if not destination.exists():
        shutil.copy2(source, destination)
        copied_count += 1

    new_item = dict(item)
    new_item["labels"] = filtered_labels
    filtered_records.append(new_item)

    for label in filtered_labels:
        class_counts[label["category"]] += 1

# ===== 4. LUU JSON =====
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(filtered_records, f, ensure_ascii=False, indent=2)

print("=== KET QUA LOC ===")
print("Anh duoc luu:", len(filtered_records))
print("Anh moi duoc sao chep:", copied_count)
print("Anh khong tim thay:", len(missing_images))
print("JSON dau ra:", OUTPUT_JSON)
print("Thu muc anh:", OUTPUT_IMAGES)

print("\n=== SO BOUNDING BOX DA GIU ===")
for cls in sorted(TARGET_CLASSES):
    print(f"{cls}: {class_counts[cls]:,}")

if missing_images:
    print("\n5 ten anh khong tim thay:")
    for name in missing_images[:5]:
        print(name)
