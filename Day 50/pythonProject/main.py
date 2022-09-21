from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# EMAIL = 
# PASSWORD = 

service = Service(ChromeDriverManager().install())
print(service.path)
driver = webdriver.Chrome(service=service)

driver.get("https://tinder.com/")
driver.maximize_window()

time.sleep(2)


log_in = driver.find_element(By.LINK_TEXT, "Log in")
log_in.click()

time.sleep(2)

log_in_with_facebook = driver.find_element(By.XPATH, '//*[@id="o-1687095699"]/div/div/div[1]/div/div[3]/span/div[2]/button')
log_in_with_facebook.click()

time.sleep(3)

# switching the window to enter email
facebook_window = driver.window_handles[1]
driver.switch_to.window(facebook_window)
driver.maximize_window()

accept_cookies = driver.find_elements(By.CSS_SELECTOR, 'button')
accept_cookies[1].click()

time.sleep(2)

email = driver.find_element(By.ID, 'email')
email.send_keys(EMAIL)
password = driver.find_element(By.ID, 'pass')
password.send_keys(PASSWORD)
facebook_login = driver.find_element(By.NAME, 'login')
facebook_login.click()

time.sleep(5)

driver.switch_to.window(driver.window_handles[0])  # switching to main Tinder window

time.sleep(5)

webdriver.ActionChains(driver).send_keys(Keys.LEFT).perform()

time.sleep(100)


