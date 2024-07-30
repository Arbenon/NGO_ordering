from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import os

# Налаштування Chrome
chrome_options = Options()

# Вказати шлях до профілю
chrome_options.add_argument("profile-directory=Yevhenii Stakhovskyi")  # Змінюйте "Default" на назву вашого профілю, якщо потрібно

# Запуск Chrome з вказаним профілем
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    driver.get("https://e.land.gov.ua/back/service/main")
    time.sleep(30)
except TimeoutException:
    print("Failed to load the main page.")
    driver.quit()
    exit()

# Натискання на "Інформація про права"
try:
    rights_info_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Інформація про права')]"))
    )
except TimeoutException:
    try:
        rights_info_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Інформація про права"))
        )
    except TimeoutException:
        try:
            rights_info_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='Інформація про права']"))
            )
        except TimeoutException:
            print("Failed to find 'Інформація про права' link.")
            driver.quit()
            exit()

if rights_info_link:
    rights_info_link.click()

def process_cadastral_number(driver, cadastral_number):
    # Натискання на "Пошук інформації"
    try:
        search_info_link = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Пошук інформації')]"))
        )
    except TimeoutException:
        try:
            search_info_link = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Пошук інформації"))
            )
        except TimeoutException:
            try:
                search_info_link = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='Пошук інформації']"))
                )
            except TimeoutException:
                print("Failed to find 'Пошук інформації' link.")
                return False

    if search_info_link:
        search_info_link.click()

    time.sleep(2)

    try:
        cadastral_number_field = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Вкажіть кадастровий номер земельної ділянки, на яку Ви бажаєте отримати інформацію')]/following-sibling::input"))
        )
        cadastral_number_field.send_keys(cadastral_number)
    except TimeoutException:
        print(f"Failed to find cadastral number field for {cadastral_number}.")
        return False

    time.sleep(2)

    cadastral_number_field.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(Keys.SPACE)

    time.sleep(2)

    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(Keys.ENTER)

    time.sleep(2)
    return True

# Перевірка наявності і читання файлу
file_path = "cadastral.txt"

# Перевірка, чи файл існує
if not os.path.isfile(file_path):
    print(f"File '{file_path}' does not exist.")
    # Виводимо список файлів у поточному каталозі
    print("Files in the current directory:")
    for file_name in os.listdir('.'):
        print(file_name)
    driver.quit()
    exit()

with open(file_path, "r") as file:
    cadastral_numbers = file.readlines()

# Очищення пробілів і символів переведення рядка
cadastral_numbers = [line.strip() for line in cadastral_numbers if line.strip()]

if not cadastral_numbers:
    print(f"The file '{file_path}' is empty or contains only whitespace.")
    driver.quit()
    exit()

# Ітерація по кадастровим номерам
for number in cadastral_numbers:
    if number:  # Пропускаємо пусті строки
        success = process_cadastral_number(driver, number)
        if not success:
            print(f"Failed to process cadastral number: {number}")
            break

driver.quit()