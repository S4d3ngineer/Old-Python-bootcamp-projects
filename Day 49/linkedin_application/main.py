from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os

service = Service(ChromeDriverManager().install())
print(service.path)
driver = webdriver.Chrome(service=service)

driver.get(os.getenv("URL"))
driver.maximize_window()

sign_in = driver.find_element(By.LINK_TEXT, "Sign in")
sign_in.click()

time.sleep(1)


username = driver.find_element(By.ID, "username")
username.send_keys(os.getenv('EMAIL'))
password = driver.find_element(By.ID, "password")
password.send_keys(os.getenv("PASSWORD") + Keys.ENTER)

time.sleep(3)

job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-card-container__metadata-item")
# job_texts = [element.text for element in job_elements]
# print(job_texts)

for element in job_elements:
    element.click()

    time.sleep(2)

    try:
        save = driver.find_element(By.CSS_SELECTOR, ".jobs-save-button")
        save.click()
    except NoSuchElementException:
        print(f"Couldn't find 'Save' button.")

    time.sleep(4)

    try:
        follow = driver.find_element(By.CSS_SELECTOR, ".follow")
        follow.click()
    except NoSuchElementException:
        print("Couldn't find 'Follow' button.")
    time.sleep(2)

time.sleep(1000)
