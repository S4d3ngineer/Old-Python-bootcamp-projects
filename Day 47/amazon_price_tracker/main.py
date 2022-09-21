import requests
from bs4 import BeautifulSoup
import lxml
from notification import Notification

PRODUCT_URL = "https://www.amazon.com/Functional-Training-Beyond-Building-Superfunctional/dp/164250503X/" \
              "ref=sr_1_1?crid=K4PDYRTQX6KK&keywords=adam+sinicki&qid=1644747569&sprefix" \
              "=adam+sinicki%2Caps%2C165&sr=8-1"

header = {
    "Accept-Language": "en,pl-PL;q=0.9,pl;q=0.8,en-US;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

with requests.get(PRODUCT_URL, headers=header) as r:
    r.raise_for_status()
    response = r.text

soup = BeautifulSoup(response, "lxml")
# print(soup.prettify())
price = float(soup.select_one("div.a-column span.a-size-medium#price").getText().strip("$"))
name = soup.select_one("h1.a-spacing-none span.a-size-extra-large#productTitle").getText()
threshold_price = 20

notification = Notification()
notification.send(price=price, name=name, threshold=threshold_price, url=PRODUCT_URL)
