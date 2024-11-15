import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import telebot
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://wsp.kbtu.kz/RegistrationOnline")
    bot.send_message(chat_id, "I am starting the bot")
    while True:
        try:
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, '//*[@id="gwt-uid-4"]'))
            # )
            time.sleep(5)
            login_form = driver.find_element(By.XPATH, '//*[@id="gwt-uid-4"]')
            password_form = driver.find_element(By.XPATH, '//*[@id="gwt-uid-6"]')

            login_form.send_keys(login)
            time.sleep(2)
            password_form.send_keys(password)
            time.sleep(2)
            password_form.send_keys(Keys.ENTER)
            time.sleep(5)
            # print("I am logged in")



        except:
            # print("auth form not found will find attend element")
            buttons = driver.find_elements(By.XPATH,
                                           '//*[@id="RegistrationOnline-1674962804"]/div/div[2]/div/div[2]/div/div/div/div/div/div/div[3]/div')

            if buttons:
                for button in buttons:
                    class_attribute = button.get_attribute("class")
                    if "v-disabled" not in class_attribute:
                        try:
                            button.click()
                            # print("click attend")
                            form = driver.find_element(By.XPATH,
                                                       '//*[@id="RegistrationOnline-1674962804"]/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div')
                            bot.send_message(chat_id, "I clicked attend \n" + form.text)
                            continue
                        except:
                            bot.send_message(chat_id, "I can't click attend, click by yourself")
                            continue
                    # print("no attend button")
            # print("refreshing")
            # bot.send_message(chat_id, "I will refresh the page")
            time.sleep(60)
            driver.refresh()
except Exception as e:
    bot.send_message(chat_id, "I am stopping the bot")
    bot.send_message(chat_id, e)
    # print(e)
