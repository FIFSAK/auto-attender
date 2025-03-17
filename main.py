import time
import os
from dotenv import load_dotenv
from kafkaClient import kafka_send
from bot import bot, TELEGRAM_CHAT_ID

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


load_dotenv()
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    kafka_send("healthy", "Bot started. Opening page...")
    driver.get("https://wsp.kbtu.kz/RegistrationOnline")
    cycle = 0
    while True:
        if cycle >= 180:
            driver.quit()
            time.sleep(2)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        cycle += 1
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

            kafka_send("healthy", "Attempted to log in. Checking for attend button...")

        except NoSuchElementException:
            pass
        except Exception as e:
            kafka_send("error", f"Unexpected error while logging in: {e}")
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
                            form = driver.find_element(
                                By.XPATH,
                                '//*[@id="RegistrationOnline-1674962804"]/div/div[2]/div/div[2]/div/div/div/div/div['
                                '1]/div/div[1]/div'
                            )
                            bot.send_mesage(TELEGRAM_CHAT_ID, "I clicked attend.\n" + form.text)
                        except Exception as e:
                            kafka_send("error", f"I can't click attend, error: {e}")
            else:
                pass

        except Exception as e:
            kafka_send("error", f"Error while searching buttons: {e}")  # error
            exit(1)

        time.sleep(60)
        driver.refresh()

except Exception as e:
    kafka_send("error", f"Bot encountered a fatal error and is stopping: {e}")  # error
    exit(1)

finally:
    driver.quit()
    kafka_send("error", "Bot stopped.")  # unhealth
