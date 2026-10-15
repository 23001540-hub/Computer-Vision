
import json
from pathlib import Path

# Đường dẫn đến file nhãn train
JSON_PATH = Path(
    "D:/bdd100k/bdd100k_labels_release/labels/bdd100k_labels_images_train.json"
)

# Kiểm tra file có tồn tại không
if not JSON_PATH.exists():
    print("KHONG TIM THAY FILE!")
    print("Duong dan dang kiem tra:", JSON_PATH)

else:
    # Đọc dữ liệu JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Kieu du lieu:", type(data).__name__)
    print("Tong so ban ghi:", len(data))

    # Xem thông tin ảnh đầu tiên
    if isinstance(data, list) and len(data) > 0:
        item = data[0]

        print("\n=== THONG TIN ANH DAU TIEN ===")
        print("Cac truong:", item.keys())
        print("Ten anh:", item.get("name"))
        print("Thuoc tinh anh:", item.get("attributes"))

        labels = item.get("labels", [])
        print("So doi tuong:", len(labels))

        if labels:
            print("\n=== NHAN DOI TUONG DAU TIEN ===")
            print(labels[0])
