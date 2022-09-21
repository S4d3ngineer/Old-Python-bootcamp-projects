from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "C:\Development\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# driver.get("https://en.wikipedia.org/wiki/Main_Page")
# # article_count = driver.find_element(By.CSS_SELECTOR, "div#articlecount a")
# # print(article_count.text)
# #
# # article_count.click()
#
# search = driver.find_element(By.NAME, "search")
# search.send_keys("Nikola Tesla")
# search.send_keys(Keys.ENTER)
#
# result = driver.find_element(By.LINK_TEXT, "Nikola Tesla")
# result.click()

driver.get("https://secure-retreat-92358.herokuapp.com/")
first_name = driver.find_element(By.NAME, "fName")
first_name.send_keys("Simon")
last_name = driver.find_element(By.NAME, "lName")
last_name.send_keys("Fucking")
email = driver.find_element(By.NAME, "email")
email.send_keys("Cowell@ihate.com")

button = driver.find_element(By.TAG_NAME, "button")
button.click()



# driver.quit()
