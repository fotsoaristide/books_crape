from bs4 import BeautifulSoup
import requests
import pandas as pd
from itertools import islice

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"


response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
     

titre = soup.find("h1").get_text(strip=True)
category = soup.find("ul", class_="breadcrumb").find_all("li")[2].get_text(strip=True)
availability = soup.find("p", class_="instock availability").get_text(strip=True)
description = soup.find("meta", attrs={"name": "description"})["content"].strip()
rating_class = soup.find("p", class_="star-rating")["class"]
rating = rating_class[1] if len(rating_class) > 1 else "No rating"
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
    "url": url,
    "category": category,
    "title": titre,
    "number_available": availability,
    "review_rating": rating,
    "image_url": image_url,
    "product_description": description,
}

book_data = {}
for k, v in book_info.items():
    book_data[k] = v
    if k == "title":
        book_data.update(table_info)



df = pd.DataFrame([book_data])
df.to_csv("book_info.csv", index=False)

print("Information du livre enregistrée dans book_info.csv")