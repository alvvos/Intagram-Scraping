from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
MAX_TIME_LOAD = 30
MIN_TIME_LOAD = 2

xpath = {
    "decline_cookies": "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]",
    "save_login_not_now_button": "//div[contains(text(), 'Ahora no')]",
    "notification_not_now_button": "//div[contains(text(), 'Ahora no')]",
    "followers_button": "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a",  # XPath para seguidores
    "following_button": "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[3]/div/a",  # XPath para seguidos
    "modal_followers": "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div",  # Modal de seguidores
    "modal_following": "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div",  # Modal de seguidos (es el mismo)
}

class InstaBot:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def close_browser(self):
        self.driver.close()

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        WebDriverWait(self.driver, MIN_TIME_LOAD)

        try:
            cookie_warning = WebDriverWait(self.driver, MIN_TIME_LOAD).until(
                EC.presence_of_element_located((By.XPATH, xpath["decline_cookies"]))
            )
            cookie_warning.click()
        except:
            pass

        username = self.driver.find_element(by=By.NAME, value="username")
        password = self.driver.find_element(by=By.NAME, value="password")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)

        try:
            save_login_prompt = WebDriverWait(self.driver, MIN_TIME_LOAD).until(
                EC.presence_of_element_located((By.XPATH, xpath["save_login_not_now_button"]))
            )
            save_login_prompt.click()
        except:
            pass

        try:
            notifications_prompt = WebDriverWait(self.driver, MIN_TIME_LOAD).until(
                EC.presence_of_element_located((By.XPATH, xpath["notification_not_now_button"]))
            )
            notifications_prompt.click()
        except:
            pass

    def find_non_followers(self):
    
        self.driver.get(f"https://www.instagram.com/{USERNAME}/")
        WebDriverWait(self.driver, MAX_TIME_LOAD).until(
            EC.presence_of_element_located((By.XPATH, xpath["followers_button"]))
        ).click()

        followers = self.get_span_content_from_modal()

        self.driver.get(f"https://www.instagram.com/{USERNAME}/")
        WebDriverWait(self.driver, MAX_TIME_LOAD).until(
            EC.presence_of_element_located((By.XPATH, xpath["following_button"]))
        ).click()

        following = self.get_span_content_from_modal()

        non_followers = [user for user in following if user not in followers]
        print("Usuarios que sigues pero que no te siguen de vuelta:")
        for user in non_followers:
            print(user)

    def get_span_content_from_modal(self):
        modal = WebDriverWait(self.driver, MAX_TIME_LOAD).until(
            EC.presence_of_element_located((By.XPATH, xpath["modal_followers"]))
        )
        
        for _ in range(10): 
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            WebDriverWait(self.driver, MIN_TIME_LOAD)

        spans = modal.find_elements(By.TAG_NAME, "span")
        span_content = [span.text for span in spans]
        
        return span_content


bot = InstaBot()
bot.login()
bot.find_non_followers()
bot.close_browser()

