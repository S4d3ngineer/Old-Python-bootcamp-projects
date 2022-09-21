from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

service = Service(ChromeDriverManager().install())
print(service.path)
driver = webdriver.Chrome(service=service)

driver.get("http://orteil.dashnet.org/experiments/cookie/")
driver.maximize_window()
cookie = driver.find_element(By.CSS_SELECTOR, "#cookie")

after_5s = time.time() + 5
after_5m = time.time() + 5 * 60

# shop_data = driver.find_elements(By.CSS_SELECTOR, "#store div")[:8]  # getting UUIDs of shop web elements
# print(shop_data)
# shop_ids = [data.get_attribute("id") for data in shop_data][::-1]  # getting lists of ids from web elements
# print(shop_ids)


# def buy_highest_tier_available():
#     for shop_id in shop_ids:
#         price = int(driver.find_element(By.CSS_SELECTOR, f"#{shop_id} b").text.split('- ')[1].replace(',', ''))
#         money = int(driver.find_element(By.CSS_SELECTOR, "#money").text.replace(',', ''))
#         while money > price:
#             driver.find_element(By.CSS_SELECTOR, f"#{shop_id}").click()


def upgrade_offer():
    """ Updates store offer """
    shop_data = driver.find_elements(By.CSS_SELECTOR, "#store b")[:8]  # getting UUIDs of shop web elements
    shop_prices = [int(data.text.split('- ')[1].replace(',', '')) for data in shop_data]
    shop_offer = {shop_data[n]: shop_prices[n] for n in range(len(shop_data))}
    return shop_offer


def buy_upgrade(offer):
    """ Buys most expensive upgrade available """
    money = int(driver.find_element(By.CSS_SELECTOR, "#money").text.replace(',', ''))
    available_purchases = {item: price for (item, price) in offer.items() if money > price}
    most_expensive_offer = max(available_purchases, key=available_purchases.get)
    if money > available_purchases[most_expensive_offer]:
        most_expensive_offer.click()


while not time.time() > after_5m:
    cookie.click()
    if time.time() > after_5s:
        shop_offer = upgrade_offer()
        buy_upgrade(offer=shop_offer)
        after_5s = time.time() + 5

cps = driver.find_element(By.CSS_SELECTOR, "#cps")
print(cps.text)

