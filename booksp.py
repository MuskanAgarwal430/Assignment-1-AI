import requests
from bs4 import BeautifulSoup
import csv
import os

BASE_URL = "http://books.toscrape.com/"
OUTPUT_CSV = "books.csv"

def get_soup(url):
    return BeautifulSoup(requests.get(url).text, "html.parser")

def scrape_book_details(book_url):
    soup = get_soup(book_url)
    description = soup.select_one("#product_description ~ p")
    return description.text.strip() if description else ""

def scrape_books():
    books_data = []
    next_url = "catalogue/page-1.html"
    while next_url:
        soup = get_soup(BASE_URL + next_url)
        for article in soup.select(".product_pod"):
            title = article.h3.a["title"]
            price = article.select_one(".price_color").text[1:]
            availability = article.select_one(".availability").text.strip()
            rating = article.p["class"][1]
            book_page = BASE_URL + "catalogue/" + article.h3.a["href"]
            image_url = BASE_URL + article.img["src"].replace("../", "")
            description = scrape_book_details(book_page)

            books_data.append({
                "title": title,
                "price": price,
                "stock": availability,
                "rating": rating,
                "image_url": image_url,
                "description": description,
                "book_page": book_page
            })

        next_btn = soup.select_one(".next > a")
        if next_btn:
            next_url = "catalogue/" + next_btn["href"]
        else:
            break
    return books_data

def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

# Run the scraper
books = scrape_books()
save_to_csv(books, OUTPUT_CSV)
print(f"Saved {len(books)} books to {OUTPUT_CSV}")
