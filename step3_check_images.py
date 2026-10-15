
from pathlib import Path

ROOT = Path("D:/bdd100k/bdd100k/images/100k")

IMAGE_EXTS = {".jpg", ".jpeg", ".png"}

for split in ["train", "val", "test"]:
    split_dir = ROOT / split

    print(f"\n===== {split.upper()} =====")

    if not split_dir.exists():
        print("Khong tim thay:", split_dir)
        continue

    # Đếm toàn bộ ảnh trong thư mục và các thư mục con
    images = [
        p for p in split_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    ]

    print("Tong so anh:", len(images))

    # Thống kê riêng từng thư mục con
    for folder in sorted(split_dir.iterdir()):
        if folder.is_dir():
            count = sum(
                1 for p in folder.rglob("*")
                if p.is_file()
                and p.suffix.lower() in IMAGE_EXTS
            )
            print(f"{folder.name}: {count:,} anh")

    # Số ảnh nằm trực tiếp trong thư mục
    direct_count = sum(
        1 for p in split_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )
    print("Anh nam truc tiep:", direct_count)
