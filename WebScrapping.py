import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


url = input("Enter URL: ")
data = {'Product Name': [], 'Price': []}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"HTTP Request failed: {e}")
    sys.exit(1)

soup = BeautifulSoup(response.text, 'html.parser')
divProduct1 = soup.select("div.KzDlHZ")
divPrice1 = soup.select("div.Nx9bqj._4b5DiR")

for product, price in zip(divProduct1, divPrice1):
    data["Product Name"].append(product.text)
    data["Price"].append(price.text)

divProduct2 = soup.select("div.syl9yP")
divPrice2 = soup.select("div.Nx9bqj")
for product, price in zip(divProduct2, divPrice2):
    data["Product Name"].append(product.text)
    data["Price"].append(price.text)

new_df = pd.DataFrame.from_dict(data)


file_path = "D:/Project/Scraped.xlsx"

if os.path.exists(file_path):
    existing_df = pd.read_excel(file_path)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
else:
    combined_df = new_df


combined_df.to_excel(file_path, index=False)

print(f"Data appended and saved to {file_path}")
