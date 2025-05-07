import sys
import os
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config

class CryptoPreprocessor:
    def __init__(self, filename):
        self.filename = filename
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def get_tokens(self):
        tokens = []
        with open(self.filename, 'r', encoding='utf-8') as file:
            for line in file:
                symbol = line.strip()
                if symbol.endswith('-USD'):
                    token = symbol[:-4]  # Bỏ '-USD'
                else:
                    token = symbol
                tokens.append(token)
        return tokens
    
    def load_crypto_history(self, symbol, limit=7):
        data = []
        file_path = os.path.join(config.HISTORY_DATA_DIR, f"{symbol}-USD.csv")
        # file_path = rf"{config.HISTORY_DATA_DIR}/{symbol}.csv"
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i > limit:
                    break
                data.append(row)
        return data[1:]
    
    def format_prompt(self, data, symbol):
        prompt = f"Lịch sử giá gần nhất của {symbol}:\n"
        prompt += "Ngày | Giá mở cửa | Giá đóng cửa | Cao nhất | Thấp nhất | Khối lượng\n"
        prompt += "-"*60 + "\n"
        for row in data:
            prompt += f"{row[1]} | {row[2]} | {row[5]} | {row[3]} | {row[4]} | {row[-1]}\n"
        return prompt
        

def main():
    crypto_preprocessor = CryptoPreprocessor(config.CRYPTO_FILENAME)
    data = crypto_preprocessor.load_crypto_history("BTC")
    print(data)
    


if __name__ == "__main__":
    main()
