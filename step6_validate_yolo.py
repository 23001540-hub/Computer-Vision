
from pathlib import Path
from collections import Counter
import math

ROOT = Path("D:/bdd100k/night_dataset_yolo")
SPLITS = ["train", "val", "test"]
EXPECTED_CLASSES = {0, 1, 2}

total_images = 0
total_labels = 0
errors = []
class_counts = Counter()

for split in SPLITS:
    image_dir = ROOT / "images" / split
    label_dir = ROOT / "labels" / split

    images = {
        p.stem for p in image_dir.iterdir()
        if p.is_file() and p.suffix.lower() in
        {".jpg", ".jpeg", ".png", ".bmp"}
    } if image_dir.exists() else set()

    labels = {
        p.stem for p in label_dir.glob("*.txt")
    } if label_dir.exists() else set()

    print(f"\n=== {split.upper()} ===")
    print("So anh:", len(images))
    print("So file nhan:", len(labels))

    missing_labels = images - labels
    orphan_labels = labels - images

    if missing_labels:
        errors.append(
            f"{split}: {len(missing_labels)} anh thieu nhan"
        )

    if orphan_labels:
        errors.append(
            f"{split}: {len(orphan_labels)} file nhan khong co anh"
        )

    total_images += len(images)

    for label_file in sorted(label_dir.glob("*.txt")):
        total_labels += 1

        for line_number, line in enumerate(
            label_file.read_text(encoding="utf-8").splitlines(),
            start=1
        ):
            parts = line.split()

            if len(parts) != 5:
                errors.append(
                    f"{label_file.name}:{line_number} "
                    "khong co dung 5 gia tri"
                )
                continue

            try:
                cls = int(parts[0])
                x, y, w, h = map(float, parts[1:])
            except ValueError:
                errors.append(
                    f"{label_file.name}:{line_number} "
                    "co gia tri khong phai so"
                )
                continue

            if cls not in EXPECTED_CLASSES:
                errors.append(
                    f"{label_file.name}:{line_number} "
                    f"class ID khong hop le: {cls}"
                )
                continue

            if not all(map(math.isfinite, [x, y, w, h])):
                errors.append(
                    f"{label_file.name}:{line_number} "
                    "co toa do khong huu han"
                )
                continue

            if not (
                0 <= x <= 1
                and 0 <= y <= 1
                and 0 < w <= 1
                and 0 < h <= 1
            ):
                errors.append(
                    f"{label_file.name}:{line_number} "
                    "toa do nam ngoai pham vi YOLO"
                )

            class_counts[cls] += 1

print("\n========== TONG KET ==========")
print("Tong so anh:", total_images)
print("Tong so file nhan:", total_labels)
print("So bounding box theo class ID:")

for cls in sorted(EXPECTED_CLASSES):
    print(f"Class {cls}: {class_counts[cls]:,}")

print("So loi:", len(errors))

for error in errors[:30]:
    print("LOI:", error)

if not errors:
    print("PASS: Khong phat hien loi trong cac kiem tra.")
