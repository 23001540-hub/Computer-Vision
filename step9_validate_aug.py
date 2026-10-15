
from pathlib import Path

ROOT = Path(r"D:/bdd100k/night_dataset_yolo_aug")
SPLITS = ["train", "val", "test"]
EXTS = {".jpg", ".jpeg", ".png", ".bmp"}

total_images = 0
total_labels = 0
errors = []

for split in SPLITS:
    img_dir = ROOT / "images" / split
    lbl_dir = ROOT / "labels" / split

    images = [
        p for p in img_dir.iterdir()
        if p.is_file() and p.suffix.lower() in EXTS
    ]
    labels = list(lbl_dir.glob("*.txt"))

    image_stems = {p.stem for p in images}
    label_stems = {p.stem for p in labels}

    missing_labels = image_stems - label_stems
    missing_images = label_stems - image_stems

    print(f"\n=== {split.upper()} ===")
    print(f"So anh: {len(images):,}")
    print(f"So file nhan: {len(labels):,}")
    print(f"Anh thieu nhan: {len(missing_labels):,}")
    print(f"Nhãn thiếu ảnh: {len(missing_images):,}")

    if missing_labels:
        errors.append(f"{split}: ảnh thiếu nhãn")
    if missing_images:
        errors.append(f"{split}: nhãn thiếu ảnh")

    total_images += len(images)
    total_labels += len(labels)

print("\n========== TONG KET ==========")
print(f"Tong anh: {total_images:,}")
print(f"Tong file nhan: {total_labels:,}")

if errors:
    print("CAN KIEM TRA:", errors)
else:
    print("PASS: Moi anh deu co file nhan tuong ung.")
