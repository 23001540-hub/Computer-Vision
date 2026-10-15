
import json
from pathlib import Path

ROOT = Path("D:/bdd100k/bdd100k/images/100k")

JSON_PATH = Path(
    "D:/bdd100k/bdd100k_labels_release/labels/bdd100k_labels_images_train.json"
)

# Đọc danh sách tên ảnh trong JSON
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

json_names = {
    item["name"]
    for item in data
    if item.get("name")
}

# Lập danh sách tên ảnh thực tế trong train
train_dir = ROOT / "train"

image_paths = [
    p for p in train_dir.rglob("*")
    if p.is_file()
    and p.suffix.lower() in {".jpg", ".jpeg", ".png"}
]

disk_names = {p.name for p in image_paths}

matched = json_names & disk_names
json_missing = json_names - disk_names
disk_unlabeled = disk_names - json_names

print("=== DOI CHIEU JSON TRAIN VOI ANH TRAIN ===")
print("So ban ghi JSON:", len(data))
print("So ten anh duy nhat trong JSON:", len(json_names))
print("So anh thuc te trong train:", len(disk_names))
print("Ten anh khop nhau:", len(matched))
print("Ten trong JSON khong tim thay anh:", len(json_missing))
print("Anh train khong co ten trong JSON:", len(disk_unlabeled))

if json_missing:
    print("\n5 ten trong JSON khong tim thay:")
    for name in sorted(json_missing)[:5]:
        print(name)

if disk_unlabeled:
    print("\n5 anh train khong co ten trong JSON:")
    for name in sorted(disk_unlabeled)[:5]:
        print(name)
