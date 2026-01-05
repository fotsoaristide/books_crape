from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
     

titre = soup.find("h1").get_text(strip=True)
price_str = soup.find("p", class_="price_color").get_text(strip=True)
price_float = float(price_str.lstrip("£"))
availability = soup.find("p", class_="instock availability").get_text(strip=True)
description = soup.find("meta", attrs={"name": "description"})["content"].strip()
rating_class = soup.find("p", class_="star-rating")["class"]
rating = rating_class[1] if len(rating_class) > 1 else "No rating"
book_data = {
    "title": titre,
    "price": price_float,
    "availability": availability,
    "description": description,
    "rating": rating
}
df = pd.DataFrame([book_data])
df.to_csv("book_info.csv", index=False)

print("Information du livre enregistrée dans book_info.csv")