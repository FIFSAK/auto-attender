import time
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import telebot

from dotenv import load_dotenv
import os

from selenium.webdriver.support.wait import WebDriverWait

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
login = os.getenv("login")
password = os.getenv("password")
chat_id = os.getenv('CHAT_ID')

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Создаем экземпляр Service с использованием ChromeDriverManager
service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://wsp.kbtu.kz/RegistrationOnline")
bot.send_message(chat_id, "I am starting the bot")
while True:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="gwt-uid-4"]'))
        )
        login_form = driver.find_element(By.XPATH, '//*[@id="gwt-uid-4"]')
        password_form = driver.find_element(By.XPATH, '//*[@id="gwt-uid-6"]')

        login_form.send_keys(login)
        time.sleep(2)
        password_form.send_keys(password)
        time.sleep(2)
        password_form.send_keys(Keys.ENTER)
        time.sleep(5)



    except:
        # print("auth form not found will find attend element")
        buttons = driver.find_elements(By.XPATH,
                                       '//*[@id="RegistrationOnline-1674962804"]/div/div[2]/div/div[2]/div/div/div/div/div/div/div[3]/div')
        # print(buttons)
        if buttons:
            for button in buttons:
                try:
                    button.click()
                    print("click attend")
                    bot.send_message(chat_id, "I clicked attend")
                except:
                    # print("find attend element again")
                    # print("refreshing")
                    time.sleep(60)
                    driver.refresh()
        # print("refreshing")
        # bot.send_message(chat_id, "I will refresh the page")
        time.sleep(60)
        driver.refresh()

