import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_books():
    print("🚀 Connecting to the website...")
    url = "http://toscrape.com"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("❌ Connection failed.")
        return
    print("✅ Connected successfully! Extracting data...")
    soup = BeautifulSoup(response.text, "html.parser")
    
    titles_list = []
    prices_list = []
    
    # Locate all the book product cards on the webpage
    books = soup.find_all("article", class_="product_pod")
    
    for book in books:
        title = book.find("h3").find("a")["title"]
        price = book.find("p", class_="price_color").text
        
        titles_list.append(title)
        prices_list.append(price)
        
    # Organise the collected data into a table format
    data_dictionary = {
        "Book Title": titles_list,
        "Price": prices_list
    }
    df = pd.DataFrame(data_dictionary)
    
    # Export the table directly to an Excel sheet
    output_filename = "books_dataset.xlsx"
    df.to_excel(output_filename, index=False)
    print(f"🎯 Success! Open your folder to find '{output_filename}'")

# THIS IS THE CRITICAL LINE THAT MAKES THE CODE RUN
if __name__ == "__main__":
    scrape_books()


