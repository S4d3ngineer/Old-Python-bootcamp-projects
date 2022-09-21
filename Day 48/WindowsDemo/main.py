from selenium import webdriver
from selenium.webdriver.common.by import By  # class for specifying locating elements ??

chrome_driver_path = "C:\Development\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# driver.get("https://www.amazon.com/Functional-Training-Beyond-Building-Superfunctional/dp/164250503X/ref=sr_1_1?crid=K4PDYRTQX6KK&keywords=adam+sinicki&qid=1644747569&sprefix=adam+sinicki%2Caps%2C165&sr=8-1")
# price = driver.find_element(By.ID, "price")
# print(price.text)

driver.get("https://www.python.org/")
events = driver.find_elements(By.CSS_SELECTOR, "div.medium-widget.event-widget.last ul.menu a")
events_list = [event.text for event in events]
print(events_list)

dates = driver.find_elements(By.CSS_SELECTOR, "div.medium-widget.event-widget.last ul.menu time")
dates_list = [date.text for date in dates]
print(dates_list)

events_dict = {}
for n in range(len(events_list)):
    events_dict[n] = {"time": dates_list[n],
                      "name": events_list[n],
    }
print(events_dict)

driver.quit()
