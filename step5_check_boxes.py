import json
from pathlib import Path
from PIL import Image

ROOT = Path("D:/bdd100k/night_dataset")
IMAGE_DIR = ROOT / "images"
JSON_PATH = ROOT / "labels_night.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

valid_boxes = 0
invalid_boxes = 0
outside_boxes = 0
missing_images = 0

for item in data:
    image_path = IMAGE_DIR / item["name"]

    if not image_path.exists():
        missing_images += 1
        continue

    with Image.open(image_path) as img:
        width, height = img.size

    for label in item.get("labels", []):
        box = label.get("box2d")
        if not isinstance(box, dict):
            invalid_boxes += 1
            continue

        try:
            x1 = float(box["x1"])
            y1 = float(box["y1"])
            x2 = float(box["x2"])
            y2 = float(box["y2"])
        except (KeyError, TypeError, ValueError):
            invalid_boxes += 1
            continue

        if not (x2 > x1 and y2 > y1):
            invalid_boxes += 1
            continue

        valid_boxes += 1

        if (
            x1 < 0 or y1 < 0
            or x2 > width or y2 > height
        ):
            outside_boxes += 1

print("=== KIEM TRA BOUNDING BOX ===")
print("So anh trong JSON:", len(data))
print("Anh khong tim thay:", missing_images)
print("Bounding box hop le ve hinh dang:", valid_boxes)
print("Bounding box khong hop le:", invalid_boxes)
print("Bounding box vuot bien anh:", outside_boxes)
