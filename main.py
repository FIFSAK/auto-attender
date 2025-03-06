from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from dotenv import load_dotenv
import telebot
import os
import time

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    bot.send_message(chat_id, "Bot started. Opening page...")
    driver.get("https://wsp.kbtu.kz/RegistrationOnline")

    while True:
        time.sleep(5)

        try:
            login_form = driver.find_element(By.XPATH, '//*[@id="gwt-uid-4"]')
            password_form = driver.find_element(By.XPATH, '//*[@id="gwt-uid-6"]')

            login_form.clear()
            login_form.send_keys(login)
            time.sleep(1)

            password_form.clear()
            password_form.send_keys(password)
            time.sleep(1)

            password_form.send_keys(Keys.ENTER)
            time.sleep(5)

            bot.send_message(chat_id, "Attempted to log in. Checking for attend button...")

        except NoSuchElementException:
            pass
        except Exception as e:
            bot.send_message(chat_id, f"Unexpected error while logging in: {e}")
            exit(1)

        try:
            buttons = driver.find_elements(
                By.XPATH,
                '//*[@id="RegistrationOnline-1674962804"]/div/div[2]/div/div[2]/div/div/div/div/div/div/div[3]/div'
            )

            if buttons:
                for button in buttons:
                    class_attribute = button.get_attribute("class")
                    if "v-disabled" not in class_attribute:
                        try:
                            button.click()
                            time.sleep(1)
                            # Ищем описание формы после клика
                            form = driver.find_element(
                                By.XPATH,
                                '//*[@id="RegistrationOnline-1674962804"]/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div'
                            )
                            bot.send_message(chat_id, "I clicked attend.\n" + form.text)
                        except Exception as e:
                            bot.send_message(chat_id, f"I can't click attend, error: {e}")
            else:
                pass

        except Exception as e:
            bot.send_message(chat_id, f"Error while searching buttons: {e}")
            exit(1)

        time.sleep(60)
        driver.refresh()

except Exception as e:
    bot.send_message(chat_id, f"Bot encountered a fatal error and is stopping: {e}")
    exit(1)

finally:
    driver.quit()
    bot.send_message(chat_id, "Bot stopped.")


