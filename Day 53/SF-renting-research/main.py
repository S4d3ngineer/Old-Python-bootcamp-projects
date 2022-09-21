import time

from bs4 import BeautifulSoup
import requests  # you have to open and read site first in order to parse it with Beautiful Soup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSdZVa1MGSQZsOCxHhLl_TEN74nRfq9tAYOx0prsmstvcyxYDA/viewform'
ZILLOW_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C' \
             '%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A' \
             '-122.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C' \
             '%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A' \
             '%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse' \
             '%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B' \
             '%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D' \
             '%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min' \
             '%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D '

header = {
    "Accept-Language": "en,pl-PL;q=0.9,pl;q=0.8,en-US;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/98.0.4758.102 Safari/537.36",
}

# with requests.get(ZILLOW_URL, headers=header) as r:
#     content = r.text

# --------ALTERNATE METHOD OF REQUESTING PAGE CONTENT (INCLUDES STUFF JAVA-SCRIPT STUFF)--------
ser = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=ser)
driver.get(ZILLOW_URL)
time.sleep(3)
content = driver.page_source

soup = BeautifulSoup(content, "lxml")

# --------------------------------------GETTING ZILLOW DATA--------------------------------------
link_elements = soup.select(".list-card-info a")
links = [element['href'] for element in link_elements]
address_elements = soup.select(".list-card-addr")
addresses = [element.getText() for element in address_elements]
print(links)
print(addresses)
price_elements = soup.select(".list-card-price")
# price_elements = soup.select("div.list-card-price")
prices = [element.getText().split("/")[0] for element in price_elements]
print(prices)
print(f"a:{len(addresses)}, p:{len(price_elements)}, l:{len(links)}")
check = soup.select(".photo-cards li")
print(len(f'Goal: {check}'))  # this is how many instances a/p/l lists should have


def fill_form():
    """It gets links, addresses and prices from offers at zillow.com"""

    driver.get(FORM_URL)
    driver.maximize_window()

    for n in range(len(links)):

        # finding input elements and buttons
        input_elements = driver.find_elements(By.CSS_SELECTOR, "div.quantumWizTextinputPaperinputInputArea input")
        address_input = input_elements[0]
        price_input = input_elements[1]
        link_input = input_elements[2]
        send_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

        # inputting data from zillow.com
        address_input.send_keys(addresses[n])
        price_input.send_keys(prices[n])
        link_input.send_keys(links[n])
        send_button.click()

        time.sleep(1)

        # allows to fill in another answer in form
        another_answer = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
        another_answer.click()

        print(f"Progress: {n+1}/{len(links)}")
        time.sleep(2)


fill_form()
driver.quit()
