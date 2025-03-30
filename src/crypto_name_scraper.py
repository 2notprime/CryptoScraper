import requests
from bs4 import BeautifulSoup
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config

class CryptoNameScraper:
    def __init__(self, start=0, count=100):
        self.base_url = "https://finance.yahoo.com/markets/crypto/all/"
        self.start = start
        self.count = count
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_page_content(self):
        url = f"{self.base_url}?start={self.start}&count={self.count}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to fetch data, status code: {response.status_code}")
    
    def parse_data(self):
        content = self.get_page_content()
        soup = BeautifulSoup(content, 'html.parser')
        symbols = soup.find_all(class_="symbol yf-1fqyif7")
        data_list = [symbol.text.strip() for symbol in symbols]
        return data_list
    
    def save_to_file(self):
        data = self.parse_data()
        mode = "a" if os.path.exists(config.CRYPTO_FILENAME) else "w"
        with open(config.CRYPTO_FILENAME, mode, encoding="utf-8") as file:
            for symbol in data:
                file.write(symbol + "\n")
        print(f"{self.start + 1} - {self.start + self.count}: Crypto name saved to {config.CRYPTO_FILENAME}")
    
    def get_crypto_data(self):
        return self.parse_data()

def main():
    for start in range(0, 9901, 100):
        scraper = CryptoNameScraper(start=start, count=100)
        scraper.save_to_file()
    
    # Clean duplicated
    if os.path.exists(config.CRYPTO_FILENAME):
        with open(config.CRYPTO_FILENAME, "r", encoding="utf-8") as file:
            lines = file.readlines()

        seen = set()  
        unique_lines = []

        for line in lines:
            stripped_line = line.strip()
            if stripped_line not in seen:
                seen.add(stripped_line)
                unique_lines.append(stripped_line)
            else:
                print(f"Remove duplicate: {stripped_line}")

        with open(config.CRYPTO_FILENAME, "w", encoding="utf-8") as file:
            file.write("\n".join(unique_lines) + "\n")

        print(f"Total unique crypto names: {len(unique_lines)}")
    else:
        print("File not found.")

if __name__ == "__main__":
    main()
