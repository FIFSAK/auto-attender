import time
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os

from selenium.webdriver.support.wait import WebDriverWait

load_dotenv()

login = os.getenv("login")
password = os.getenv("password")

driver = webdriver.Chrome()

driver.get("https://wsp.kbtu.kz/RegistrationOnline")
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
        print("auth form not found will find attend element")
        buttons = driver.find_elements(By.XPATH,
                                       '//*[@id="RegistrationOnline-1674962804"]/div/div[2]/div/div[2]/div/div/div/div/div/div/div[3]/div')
        print(buttons)
        if buttons:
            for button in buttons:
                try:
                    button.click()
                    print("click attend")
                except:
                    print("find attend element again")
                    print("refreshing")
                    time.sleep(60)
                    driver.refresh()
        print("refreshing")
        time.sleep(60)
        driver.refresh()
