
import json
import random
import shutil
from pathlib import Path
from collections import Counter
from PIL import Image

# ==========================================
# 1. KHAI BAO DUONG DAN
# ==========================================
SOURCE_DIR = Path("D:/bdd100k/night_dataset")
IMAGE_DIR = SOURCE_DIR / "images"
JSON_PATH = SOURCE_DIR / "labels_night.json"

OUTPUT_DIR = Path("D:/bdd100k/night_dataset_yolo")

# Anh thuoc 3 lop can nhan dang
CLASS_MAP = {
    "person": 0,
    "car": 1,
    "traffic light": 2
}

# Ty le chia du lieu
TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
SEED = 42


def convert_box(box, image_width, image_height):
    """Chuyen toa do BDD100K sang toa do YOLO."""
    x1 = float(box["x1"])
    y1 = float(box["y1"])
    x2 = float(box["x2"])
    y2 = float(box["y2"])

    # Gioi han toa do trong pham vi anh
    x1 = max(0.0, min(x1, image_width))
    x2 = max(0.0, min(x2, image_width))
    y1 = max(0.0, min(y1, image_height))
    y2 = max(0.0, min(y2, image_height))

    # Bo qua box khong co kich thuoc
    if x2 <= x1 or y2 <= y1:
        return None

    # Toa do tam va kich thuoc chuan hoa
    x_center = ((x1 + x2) / 2) / image_width
    y_center = ((y1 + y2) / 2) / image_height
    width = (x2 - x1) / image_width
    height = (y2 - y1) / image_height

    return x_center, y_center, width, height


def main():
    # ==========================================
    # 2. KIEM TRA DU LIEU DAU VAO
    # ==========================================
    if not JSON_PATH.exists():
        raise FileNotFoundError(
            f"Khong tim thay file JSON: {JSON_PATH}"
        )

    if not IMAGE_DIR.exists():
        raise FileNotFoundError(
            f"Khong tim thay thu muc anh: {IMAGE_DIR}"
        )

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)

    print(f"Tong anh trong JSON: {len(records):,}", flush=True)

    # ==========================================
    # 3. CHIA TRAIN / VAL / TEST
    # ==========================================
    records = list(records)
    random.Random(SEED).shuffle(records)

    total = len(records)
    n_train = int(total * TRAIN_RATIO)
    n_val = int(total * VAL_RATIO)

    splits = {
        "train": records[:n_train],
        "val": records[n_train:n_train + n_val],
        "test": records[n_train + n_val:]
    }

    print("\nSo anh moi tap:", flush=True)
    for split_name, items in splits.items():
        print(f"{split_name}: {len(items):,}", flush=True)

    # ==========================================
    # 4. TAO CAU TRUC THU MUC
    # ==========================================
    for split_name in splits:
        (OUTPUT_DIR / "images" / split_name).mkdir(
            parents=True, exist_ok=True
        )
        (OUTPUT_DIR / "labels" / split_name).mkdir(
            parents=True, exist_ok=True
        )

    # ==========================================
    # 5. CHUYEN NHAN VA SAO CHEP ANH
    # ==========================================
    class_counts = Counter()
    copied_images = 0
    missing_images = 0
    failed_images = 0
    saved_boxes = 0

    for split_name, items in splits.items():
        out_image_dir = OUTPUT_DIR / "images" / split_name
        out_label_dir = OUTPUT_DIR / "labels" / split_name

        print(f"\nDang xu ly tap {split_name}...", flush=True)

        for i, item in enumerate(items, start=1):
            image_name = item["name"]
            source_image = IMAGE_DIR / image_name

            if not source_image.exists():
                missing_images += 1
                continue

            try:
                with Image.open(source_image) as img:
                    image_width, image_height = img.size
                    img.verify()

                # Doc lai anh sau verify de chac chan file doc duoc
                with Image.open(source_image) as img:
                    img.load()

            except Exception as e:
                failed_images += 1
                print(
                    f"Loi anh {image_name}: {e}",
                    flush=True
                )
                continue

            yolo_lines = []

            for label in item.get("labels", []):
                category = label.get("category")

                if category not in CLASS_MAP:
                    continue

                box = label.get("box2d")
                if not isinstance(box, dict):
                    continue

                try:
                    converted = convert_box(
                        box, image_width, image_height
                    )
                except (KeyError, TypeError, ValueError):
                    continue

                if converted is None:
                    continue

                x_center, y_center, width, height = converted
                class_id = CLASS_MAP[category]

                yolo_lines.append(
                    f"{class_id} "
                    f"{x_center:.6f} "
                    f"{y_center:.6f} "
                    f"{width:.6f} "
                    f"{height:.6f}"
                )

                class_counts[category] += 1
                saved_boxes += 1

            # Chi luu anh co it nhat 1 box thuoc 3 lop muc tieu
            if not yolo_lines:
                continue

            shutil.copy2(
                source_image,
                out_image_dir / image_name
            )

            label_path = out_label_dir / (
                Path(image_name).stem + ".txt"
            )
            label_path.write_text(
                "\n".join(yolo_lines) + "\n",
                encoding="utf-8"
            )

            copied_images += 1

            if i % 500 == 0 or i == len(items):
                print(
                    f"  Tien do {split_name}: "
                    f"{i:,}/{len(items):,}",
                    flush=True
                )

    # ==========================================
    # 6. TAO FILE data.yaml
    # ==========================================
    yaml_content = f"""path: {OUTPUT_DIR.as_posix()}
train: images/train
val: images/val
test: images/test

names:
  0: person
  1: car
  2: traffic light
"""

    (OUTPUT_DIR / "data.yaml").write_text(
        yaml_content,
        encoding="utf-8"
    )

    # ==========================================
    # 7. BAO CAO
    # ==========================================
    print("\n========== KET QUA CHUYEN DOI ==========")
    print(f"Anh da sao chep: {copied_images:,}")
    print(f"Anh khong tim thay: {missing_images:,}")
    print(f"Anh bi loi khi doc: {failed_images:,}")
    print(f"Tong bounding box da luu: {saved_boxes:,}")

    print("\nSo bounding box theo lop:")
    for category in CLASS_MAP:
        print(f"{category}: {class_counts[category]:,}")

    print("\nThu muc dau ra:", OUTPUT_DIR)
    print("File cau hinh:", OUTPUT_DIR / "data.yaml")
    print("\nDa hoan tat!")

if __name__ == "__main__":
    main()
