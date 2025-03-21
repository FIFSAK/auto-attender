import time
import os
import json
import datetime
from datetime import timedelta, timezone
import threading
from dotenv import load_dotenv
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import telebot
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv()

# wsp credentials
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

# Telegram config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["report"])
def status_command(message):
    response = "CURRENT STATUS:\n"
    messages = read_last_n_messages(kafka_topic, kafka_servers, n=6)

    if messages and messages[-1]["status"] == "healthy":
        response += "healthy"
    else:
        if messages:
            response += "unhealthy since " + format_timestamp(messages[-1]["timestamp"])
        else:
            response += "No messages found."

    response += "\n\nHISTORY:\n"
    for msg in messages:
        ts = format_timestamp(msg['timestamp'])
        response += f"{ts} - {msg['status']} - {msg['message']}\n"

    bot.send_message(message.chat.id, response)


def format_timestamp(ts_str):
    try:
        dt = datetime.datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        try:
            dt = datetime.datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return ts_str

    utc_offset = timezone(timedelta(hours=5))  # UTC+5
    dt = dt.replace(tzinfo=timezone.utc).astimezone(utc_offset)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def start_bot():
    """
    This function runs your Telegram bot in a loop.
    We'll start it in a background thread so our main loop can also run.
    """
    # print("Starting bot...")
    # bot.send_message(TELEGRAM_CHAT_ID, "Bot started.")
    bot.infinity_polling()  # or bot.polling(none_stop=True)


def main_loop():
    """
    This function runs the infinite Selenium logic.
    Because we want the Telegram bot to keep running, we do this in the main thread
    while the bot is in a separate thread.
    """
    try:
        # print("Starting main loop...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")

        # service = Service("/usr/bin/chromedriver")  # for docker prod
        service = Service(executable_path=ChromeDriverManager().install())  # for windows
        print("healthy", "Bot started. Opening page...")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        cycle = 0
        driver.get("https://wsp.kbtu.kz/RegistrationOnline")

        while True:
            if cycle >= 180:
                driver.quit()
                time.sleep(2)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                driver.get("https://wsp.kbtu.kz/RegistrationOnline")
                cycle = 0

            cycle += 1
            time.sleep(5)

            # Attempt to log in
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

                print("healthy", "Attempted to log in. Checking for attend button...")
            except NoSuchElementException:
                # Not on the login page or elements not found yet
                pass
            except Exception as e:
                print("error", f"Unexpected error while logging in: {e}")
                return  # or break, or pass

            # Look for attend buttons
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
                                    '//*[@id="RegistrationOnline-1674962804"]/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div'
                                )
                                print("healthy", "Clicked attend.\n" + form.text)
                                bot.send_message(TELEGRAM_CHAT_ID, "I clicked attend.\n" + form.text)
                            except Exception as e:
                                print("error", f"I can't click attend, error: {e}")
                else:
                    pass

            except Exception as e:
                print("error", f"Error while searching buttons: {e}")
                return

            time.sleep(60)
            driver.refresh()

    except Exception as e:
        print("error", f"Bot encountered a fatal error and is stopping: {e}")
    finally:
        print("error", "Bot stopped.")


if __name__ == "__main__":
    # print("Starting main loop in a separate thread...")
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    main_loop()
