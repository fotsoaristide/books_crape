import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import islice
from urllib.parse import urljoin
import os

url = "https://books.toscrape.com/"

def get_book_urls(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")
    book_links = soup.select("h3 a")
    book_urls = [urljoin(category_url, link['href']) for link in book_links]
    return book_urls

def safe_filename(name):
    return "".join(c.lower() if c.isalnum() else "_" for c in name).strip("_")


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
    

    safe_category = category.replace(" ", "_").lower()
    folder = os.path.join("images", safe_category)
    os.makedirs(folder, exist_ok=True)

    image_name = safe_filename(title) + ".jpg"
    local_image_path = os.path.join(folder, image_name)
    img_response = requests.get(image_url, stream=True)
    img_response.raise_for_status()

    with open(local_image_path, "wb") as img_file:
        for chunk in img_response.iter_content(1024):
            img_file.write(chunk)

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
    
def category_pagination_urls(category_url):
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

def get_all_categories():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    categories = {}
    category_links = soup.select(".side_categories ul li ul li a")
    for link in category_links:
        category_name = link.get_text(strip=True)
        category_url = urljoin(url, link['href'])
        categories[category_name] = category_url
    return categories

for category_name, category_url in get_all_categories().items():
    print(f"Scraping category: {category_name}")

    books = []

    for page_url in category_pagination_urls(category_url):
        book_urls = get_book_urls(page_url)
        for book_url in book_urls:
            book_data = scrape_book_data(book_url)
            books.append(book_data)

    df = pd.DataFrame(books)
    csv_filename = f"{category_name.replace(' ', '_').lower()}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Saved data for category '{category_name}' to {csv_filename}")

print("Scraping completed.")    




