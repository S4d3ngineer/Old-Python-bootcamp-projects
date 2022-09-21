from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
import time

# USERNAME = 
# PASSWORD = 
SPEEDTEST_URL = 'https://www.speedtest.net/result/12780973723'
TWITTER_URL = 'https://twitter.com/'

class InternetSpeedTwitterBot:

    def __init__(self):

        # creating Selenium driver
        self.service = Service(ChromeDriverManager().install())
        print(self.service.path)
        self.driver = webdriver.Chrome(service=self.service)

        self.up = 0
        self.down = 0

    def get_internet_speed(self):

        self.driver.get(SPEEDTEST_URL)
        self.driver.maximize_window()
        time.sleep(4)
        consent = self.driver.find_element(By.ID, '_evidon-banner-acceptbutton')
        consent.click()
        time.sleep(2)
        go = self.driver.find_element(By.CSS_SELECTOR, '.start-text')
        go.click()
        time.sleep(60)
        download = self.driver.find_element(By.CSS_SELECTOR, "span.download-speed")
        self.down = float(download.text)
        upload = self.driver.find_element(By.CSS_SELECTOR, "span.upload-speed")
        self.up = float(upload.text)

    def tweet_at_provider(self):

        self.driver.get(TWITTER_URL)
        self.driver.maximize_window()
        time.sleep(2)
        sign_in = self.driver.find_element(By.LINK_TEXT, "Sign in")
        sign_in.click()
        time.sleep(3)
        input_username = self.driver.find_element(By.TAG_NAME, "input")
        input_username.send_keys(USERNAME + Keys.ENTER)
        time.sleep(2)
        input_password = self.driver.find_elements(By.TAG_NAME, "input")[1]
        input_password.send_keys(PASSWORD + Keys.ENTER)
        time.sleep(3)
        tweet_input = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
        tweet_text = f"Why is my internet speed {self.down}/{self.up} when i pay for 160/10?"
        tweet_input.send_keys(tweet_text)
        tweet_send = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span')
        tweet_send.click()
        time.sleep(3000)



