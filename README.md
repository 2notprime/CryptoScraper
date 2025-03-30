# Yahoo Finance CSV Scraper

## Mô tả

Script này crawl dữ liệu lịch sử giao dịch của các đồng tiền mã hóa từ Yahoo Finance và lưu vào các file CSV riêng biệt cho từng đồng tiền. Gồm 2 phần: Crawl symbol của các crypto (ví dụ: BTC-USD) và crawl dữ liệu lịch sử của chúng.

## Cài đặt

```bash
# Clone repository
git clone https://github.com/2notprime/CryptoScraper.git
cd CryptoScraper

# Tạo môi trường ảo
python -m venv .venv
source .venv/bin/activate  # Trên macOS/Linux
# hoặc
.venv\Scripts\activate    # Trên Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

## Cấu hình

Kiểm tra file `config.py` và điền các thông tin cần thiết:

```python
CRYPTO_FILENAME = "data/crypto_symbols.txt"
HISTORY_DATA_DIR = "data/crypto_history"
```

## Cách sử dụng

Lưu ý: Code hiện tại chỉ đang chạy mẫu 3 samples đầu để push data mẫu,
nếu muốn chạy toàn bộ vui lòng xóa dòng 70: symbols = symbols[:3]
trong file (src/crypto_history_scraper.py)

Phần 1: Crawl symbols

```bash
python -u .\src\crypto_name_scraper.py
```

Phần 2: Crawl history

```bash
python -u .\src\crypto_history_scraper.py
```

## Kết quả

Các file CSV sẽ được lưu trong thư mục `crypto_history/`, mỗi file tương ứng với một mã crypto.
