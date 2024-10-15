from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.window import WindowTypes
import time
import requests


CHROME_DRIVER_PATH = "C:\\Users\\97258\\Desktop\\chromedriver-win64\\chromedriver.exe"


def openChrome(link):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(link)
    driver.set_window_size(1600, 1000)
    return driver


def open_new_window_for_match(driver, match_link):
    # Open a new window
    driver.switch_to.new_window(WindowTypes.WINDOW)

    # Navigate to the match link in the new window
    driver.get(match_link)


def login_mhfc(driver, username, password):


    wait = WebDriverWait(driver, 10)  # Define wait here
    driver.find_element(By.NAME, 'email').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    # Wait for the login button and click it
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="התחבר"]')))
    login_button.click()


def close_cookies(driver):
    driver.find_element(By.XPATH, '//span[text()="close"]').click()
    driver.find_element(By.XPATH, '//span[@class="material-symbols-outlined" and text()="done"]').click()


def choose_location(driver,section,numOfTickets):
    driver.find_element(By.XPATH, '//i[text()="expand_more" and contains(@class, "material-icons")]').click()
    driver.find_element(By.XPATH, '//li[contains(text(), "גוש 502")]').click()
    # Wait for the input field to be interactable
    numOfTickets_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'scount')))
    numOfTickets_field.clear()
    numOfTickets_field.send_keys(str(numOfTickets))
    driver.find_element(By.ID, 'fnFastSeats').click()
    """send_telegram_message("i found tickets to:", section)"""


def send_telegram_message(message, section_num): #send telegram messege that a ticket has been found
    chat_id = "-819945328"
    bot_token = "5859153132:AAHva7RSPGoN1XQ_DD1EcHwRaWrw-ozzpVk"
    base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": f"{message}\nSection Number: {section_num}",  # Include section_num in the message
    }

    response = requests.post(base_url, params=params)
    '''if response.ok:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Error code: {response.status_code}, Error message: {response.text}")'''

if __name__ == "__main__":
    username = "yardentziar@gmail.com"
    password = "Almog1234!"
    login_link = "https://auth.mhaifafc.com/login"
    match_link = "https://tickets.mhaifafc.com/Stadium/Index?eventId=3190"

    driver = openChrome(login_link)
    login_mhfc(driver, username, password)
    time.sleep(3)
    open_new_window_for_match(driver, match_link)
    close_cookies(driver)
    time.sleep(3)
    choose_location(driver,502,2)
    time.sleep(3000)

