import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import os

load_dotenv()

login = os.getenv("login")
password = os.getenv("password")


login = os.getenv("login")
password = os.getenv("password")

driver = webdriver.Chrome()

# открыть страницу
driver.get("https://wsp.kbtu.kz/RegistrationOnline")
while True:
    try:
        time.sleep(5)
        login_form = driver.find_elements(By.XPATH, '//*[@id="gwt-uid-4"]')
        password_form = driver.find_elements(By.XPATH, '//*[@id="gwt-uid-6"]')
        buttons = driver.find_elements(By.XPATH, "//span[@class='v-button-caption' and contains(text(), 'Отметиться')]")
        if login_form and password:
            login_form[0].send_keys(login)
            password_form[0].send_keys(password)
            password_form[0].send_keys(Keys.ENTER)
            time.sleep(5)
        else:
            print("form not found")
        if buttons:
            for button in buttons:
                button.click()
        else:
            print("Кнопка 'Отметиться' не найдена")
            time.sleep(5)
            driver.refresh()
    except NoSuchElementException:
        print("Элемент не найден")

