from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

INSTAGRAM_LOGIN_URL = 'https://www.instagram.com/accounts/login/'
INSTAGRAM_URL = "https://www.instagram.com/"
SIMILAR_ACCOUNT = 'deathandmilk_/'

# USERNAME = 
# PASSWORD = 
SCROLL_PAUSE_TIME = 0.5


class InstaFollower:

    def __init__(self):

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):

        self.driver.get(INSTAGRAM_LOGIN_URL)
        self.driver.maximize_window()
        time.sleep(2)
        accept_cookies = self.driver.find_element(By.CSS_SELECTOR, ".aOOlW.bIiDR")
        accept_cookies.click()
        time.sleep(2)
        elements = self.driver.find_elements(By.TAG_NAME, "input")
        username = elements[0]
        password = elements[1]
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD + Keys.ENTER)
        # sqdOP.yWX7d.y3zKF

    def find_followers(self):

        self.driver.get(INSTAGRAM_URL + SIMILAR_ACCOUNT)
        time.sleep(2)
        # following_button = self.driver.find_element(By.CLASS_NAME, "g47SY")
        following_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[3]/a/div/span')
        following_button.click()
        time.sleep(3)
        pop_up = self.driver.find_element(By.CLASS_NAME, "isgrP")

        keep_scrolling = True
        while keep_scrolling:
            last_height = self.driver.execute_script("return arguments[0].scrollHeight", pop_up)
            print(f'last height: {last_height}')
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up)
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", pop_up)
            print(f'new height:{new_height}')
            if last_height == new_height:
                time.sleep(2)
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up)
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", pop_up)
                if last_height == new_height:
                    keep_scrolling = False

    def follow(self):
        follower_list_class = "PZuss"
        # I am using following rather than followers to reduce its number for testing purposes
        following_list = self.driver.find_elements(By.CSS_SELECTOR, f".{follower_list_class} button")
        # single_following = self.driver.find_element(By.LINK_TEXT, "Follow")
        for follower in following_list:
            n = 1
            if follower.text == "Follow":
                follower.click()
                # element = self.wait.until(EC.element_to_be_clickable(follower))
                while follower.text != "Following":
                    time.sleep(0.1)
                print(f"Follower {n}/{len(following_list)} has been followed.")
                n += 1
            # -------- unused code -------- #
            # try:
            #     time.sleep(1)
            #     follower.click()
            # except ElementClickInterceptedException:
            #     cancel_button = self.driver.find_element(By.CSS_SELECTOR, ".aOOlW.HoLwm")
            #     cancel_button.click()
            # -------- unused code -------- #


insta = InstaFollower()
insta.login()
time.sleep(2)
insta.find_followers()
time.sleep(2)
insta.follow()
