
import random
import shutil
from pathlib import Path
from PIL import Image, ImageEnhance

# ==========================================
# 1. DUONG DAN DU LIEU
# ==========================================
SOURCE_DIR = Path(r"D:/bdd100k/night_dataset_yolo")
OUTPUT_DIR = Path(r"D:/bdd100k/night_dataset_yolo_aug")

SPLITS = ["train", "val", "test"]
SEED = 42

# Cac dinh dang anh duoc ho tro
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}

random.seed(SEED)


def augment_image(image):
    """
    Tang cuong anh bang cach thay doi do sang
    va do tuong phan. Khong thay doi hinh hoc.
    """
    # Thay doi do sang trong khoang 0.70 den 1.30
    brightness_factor = random.uniform(0.70, 1.30)
    image = ImageEnhance.Brightness(image).enhance(
        brightness_factor
    )

    # Thay doi do tuong phan trong khoang 0.85 den 1.20
    contrast_factor = random.uniform(0.85, 1.20)
    image = ImageEnhance.Contrast(image).enhance(
        contrast_factor
    )

    return image


def main():
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(
            f"Khong tim thay du lieu: {SOURCE_DIR}"
        )

    total_originals = 0
    total_augmented = 0
    total_labels = 0

    for split in SPLITS:
        source_images = SOURCE_DIR / "images" / split
        source_labels = SOURCE_DIR / "labels" / split

        output_images = OUTPUT_DIR / "images" / split
        output_labels = OUTPUT_DIR / "labels" / split

        output_images.mkdir(parents=True, exist_ok=True)
        output_labels.mkdir(parents=True, exist_ok=True)

        image_paths = sorted(
            p for p in source_images.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS
        )

        print(f"\n=== {split.upper()} ===", flush=True)
        print(f"So anh goc: {len(image_paths):,}", flush=True)

        for i, image_path in enumerate(image_paths, start=1):
            label_path = source_labels / (
                image_path.stem + ".txt"
            )

            if not label_path.exists():
                raise FileNotFoundError(
                    f"Thieu nhan cho anh: {image_path.name}"
                )

            # Sao chep anh goc va nhan goc
            shutil.copy2(
                image_path,
                output_images / image_path.name
            )
            shutil.copy2(
                label_path,
                output_labels / label_path.name
            )

            total_originals += 1
            total_labels += 1

            # Chi tang cuong tap train
            if split == "train":
                try:
                    with Image.open(image_path) as img:
                        image = img.convert("RGB")
                        augmented = augment_image(image)

                        aug_name = (
                            image_path.stem
                            + "_aug"
                            + image_path.suffix.lower()
                        )

                        augmented.save(
                            output_images / aug_name,
                            quality=95
                        )

                    # Anh chi thay doi mau sac/do sang,
                    # nen co the giu nguyen bounding box.
                    aug_label_name = (
                        image_path.stem + "_aug.txt"
                    )

                    shutil.copy2(
                        label_path,
                        output_labels / aug_label_name
                    )

                    total_augmented += 1

                except Exception as e:
                    raise RuntimeError(
                        f"Loi tang cuong {image_path.name}: {e}"
                    ) from e

            if i % 500 == 0 or i == len(image_paths):
                print(
                    f"Tien do {split}: "
                    f"{i:,}/{len(image_paths):,}",
                    flush=True
                )

    # Tao file data.yaml cho bo du lieu moi
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

    print("\n========== KET QUA AUGMENTATION ==========")
    print(f"So anh goc da sao chep: {total_originals:,}")
    print(f"So anh tang cuong: {total_augmented:,}")
    print(
        f"Tong anh trong bo moi: "
        f"{total_originals + total_augmented:,}"
    )
    print(f"So file nhan da sao chep: {total_labels:,}")
    print(f"Thu muc dau ra: {OUTPUT_DIR}")
    print("Da hoan tat!")


if __name__ == "__main__":
    main()
