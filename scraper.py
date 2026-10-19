import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Correct base URL for the book scraping sandbox
URL = "http://toscrape.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def scrape_page(url):
    print(f"Attempting to fetch: {url}")

    try:
        # Send request with network headers
        response = requests.get(url, headers=HEADERS, timeout=10)

        # Print debug statements to monitor the network stream
        print(f"--> Status Code: {response.status_code}")
        print(f"--> HTML Content Length: {len(response.text)} characters")

        if response.status_code != 200:
            print(f"❌ Failed to retrieve page. Status code: {response.status_code}")
            return []

        # Parse HTML text content
        soup = BeautifulSoup(response.text, "html.parser")
        data_list = []

        # Find the specific product containers used on books.toscrape.com
        items = soup.find_all("article", class_="product_pod")
        print(f"--> Found {len(items)} items on this page.")

        for item in items:
            # Extract the full title string from the image placeholder attribute
            title_element = item.find("h3").find("a")
            title = title_element["title"] if title_element else "N/A"

            # Extract the text from the price paragraph tag
            price_element = item.find("p", class_="price_color")
            price = price_element.text if price_element else "N/A"

            # Save only the Title and Price data fields
            data_list.append({"Title": title, "Price": price})

        return data_list

    except requests.exceptions.RequestException as e:
        print(f"❌ A connection error occurred: {e}")
        return []


def save_to_excel(data, filename="scraped_data.xlsx"):
    if not data:
        print("⚠️ No data was collected. Excel generation canceled.")
        return

    # Create structural DataFrame from list of dictionaries
    df = pd.DataFrame(data)

    try:
        df.to_excel(filename, index=False)
        print(
            f"🎉 Success! Data successfully saved to: {os.path.abspath(filename)}"
        )
    except Exception as e:
        print(f"❌ Failed to compile Excel document: {e}")


if __name__ == "__main__":
    print("--- Starting Single Page Test ---")

    # Fetch data from the initial page layout
    scraped_data = scrape_page(URL)

    # Show structural preview of retrieved records
    if scraped_data:
        print("\nData Preview:")
        for entry in scraped_data[:3]:
            print(f"- {entry}")

    print("\n--- Saving Dataset ---")
    save_to_excel(scraped_data)