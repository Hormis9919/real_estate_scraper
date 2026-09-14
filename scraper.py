import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

URL = "insert example URL here"
def scrape_listings(total_pages=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    raw_listings = []
    for page in range(1,total_pages+1):
        url = URL
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue
        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all("div", class_="property-card")
        for card in cards:
            title = card.find("h2", class_="title")
            price = card.find("span", class_="price")
            details = card.find("div", class_="details")
            location = card.find("span", class_="location")
            raw_listings.append({
                "raw_title": title.text if title else None,
                "raw_price": price.text if price else None,
                "raw_details": details.text if details else None,
                "raw_location": location.text if location else None
            })
        time.sleep(1)
    return pd.DataFrame(raw_listings)
if __name__ == "__main__":
    df_raw = scrape_listings()
    df_raw.to_csv("data/raw_scraped_listings.csv",index=False)
    print("Scraping completed. Raw data saved")