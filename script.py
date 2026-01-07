import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import islice
from urllib.parse import urljoin


CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"

books = []

def get_book_urls(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")
    book_links = soup.select("h3 a")
    book_urls = [urljoin(category_url, link['href']) for link in book_links]
    return book_urls
def scrape_book_data(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("h1").get_text(strip=True)
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].get_text(strip=True)
    availability = soup.find("p", class_="instock availability").get_text(strip=True)
    rating_class = soup.find("p", class_="star-rating")["class"]
    description = soup.find("meta", attrs={"name": "description"})["content"].strip()
    table = soup.find("table")
    table_info = {}
    for row in islice(table.find_all("tr"), 4):
        key = row.find("th").get_text(strip=True)
        value = row.find("td").get_text(strip=True).lstrip("£")
        table_info[key] = value

    img_tag = soup.find("div", class_="item active").find("img")
    img_src = img_tag["src"]
    image_url = "https://books.toscrape.com/" + img_src.replace("../../", "")

    book_info = {
        "url": book_url,
        "category": category,
        "title": title,
        "number_available": availability,
        "review_rating": rating_class[1] if len(rating_class) > 1 else "No rating",
        "image_url": image_url,
        "product_description": description,
    }
    book_data = {}
    for k, v in book_info.items():
        book_data[k] = v
        if k == "title":
            book_data.update(table_info)
    return book_data
    
def cathegory_pagination_urls(category_url):
    urls = [category_url]
    while True:
        response = requests.get(urls[-1])
        soup = BeautifulSoup(response.content, "html.parser")
        next_button = soup.find("li", class_="next")
        if next_button:
            next_page_url = urljoin(urls[-1], next_button.find("a")["href"])
            urls.append(next_page_url)
        else:
            break
    return urls

pagination_urls = cathegory_pagination_urls(CATEGORY_URL)
for page_url in pagination_urls:
    book_urls = get_book_urls(page_url)
    for book_url in book_urls:
        book_data = scrape_book_data(book_url)
        books.append(book_data)        


df = pd.DataFrame(books)
df.to_csv("books_scrape_books_sequential_art_2026_01_07.csv", index=False, encoding="utf-8")

print(f"{len(df)} livres extraits avec succès ✅")