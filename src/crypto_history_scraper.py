import requests
from bs4 import BeautifulSoup
import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config

class CryptoHistoryScraper:
    def __init__(self, symbols):
        self.symbols = symbols
        self.base_url = "https://finance.yahoo.com/quote/{}/history/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_page_content(self, symbol):
        response = requests.get(self.base_url.format(symbol), headers=self.headers)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to fetch data for {symbol}, status code: {response.status_code}")
            return None
    
    def parse_data(self, symbol):
        content = self.get_page_content(symbol)
        if not content:
            return None, None
        
        soup = BeautifulSoup(content, 'html.parser')
        
        thead = soup.find('thead', class_='yf-1jecxey')
        headers = []
        if thead:
            tr = thead.find('tr')
            headers = [th.text.strip() for th in tr.find_all('th')]
        
        tbody = soup.find('tbody')
        rows = []
        if tbody:
            for tr in tbody.find_all('tr'):
                row = [td.text.strip() for td in tr.find_all('td')]
                if row:
                    rows.append([symbol] + row)  
        
        return headers, rows
    
    def save_to_csv(self):
        os.makedirs(config.HISTORY_DATA_DIR, exist_ok=True)
        total = len(self.symbols)
        
        for index, symbol in enumerate(self.symbols, start=1):
            output_file = os.path.join(config.HISTORY_DATA_DIR, f"{symbol}.csv")
            headers, rows = self.parse_data(symbol)
            if not headers or not rows:
                print(f"No data found for {symbol}.")
                continue
            
            with open(output_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Symbol"] + headers)  
                writer.writerows(rows)
            
            print(f"{index}/{total}: Done fetching data for {symbol}, saved to {output_file}")

if __name__ == "__main__":
    with open(config.CRYPTO_FILENAME, "r", encoding="utf-8") as file:
        symbols = [line.strip() for line in file.readlines()]
    symbols = symbols[:3]
    scraper = CryptoHistoryScraper(symbols)
    scraper.save_to_csv()
