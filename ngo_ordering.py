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

# Налаштування опцій Chrome
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:\\Users\\ЄвгенійСтаховський\\AppData\\Local\\Google\\Chrome\\User Data")

# Ініціалізація драйвера
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    driver.get("https://e.land.gov.ua/back/service/main")
    time.sleep(20)
except TimeoutException:
    print("Failed to load the main page.")
    driver.quit()
    exit()

    # Пошук посилання "Відомості ДЗК" за кількома методами
try:
    info_DZK_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Відомості ДЗК')]"))
    )
except TimeoutException:
    try:
        info_DZK_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Відомості ДЗК"))
        )
    except TimeoutException:
        try:
            info_DZK_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='Відомості ДЗК']"))
            )
        except TimeoutException:
            print("Failed to find 'Інформація про права' link.")
            driver.quit()
            exit()

if info_DZK_link:
    info_DZK_link.click()

    # Пошук посилання "Замовити" за кількома методами
try:
    info_DZK_order_link = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Замовити')]"))
    )
except TimeoutException:
    try:
        info_DZK_order_link = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Замовити"))
        )
    except TimeoutException:
        try:
            info_DZK_order_link = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='Замовити']"))
            )
        except TimeoutException:
            driver.quit()
            exit("Не вдалося знайти посилання 'Замовити'")

if info_DZK_order_link:
    info_DZK_order_link.click()

def process_cadastral_number(driver, cadastral_number):
        # Вибір типу заяви
    try:
        application_type_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Тип заяви')]/following-sibling::select"))
        )
        application_type_dropdown.click()

        for _ in range(6):
            application_type_dropdown.send_keys(Keys.ARROW_DOWN)
        application_type_dropdown.send_keys(Keys.ENTER)
            
    except TimeoutException:
        driver.quit()
        exit("Не вдалося знайти або взаємодіяти з випадаючим списком 'Тип заяви'")

        # Введення кадастрового номеру
    try:
        cadastral_number_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Кадастровий номер земельної ділянки')]/following-sibling::input"))
        )
        cadastral_number_field.send_keys(cadastral_number)
    except TimeoutException:
        driver.quit()
        exit("Не вдалося знайти поле для вводу кадастрового номеру")

        # Використання TAB для переходу між полями
    for _ in range(9):
        driver.switch_to.active_element.send_keys(Keys.TAB)
        time.sleep(0.1)

        # Введення місця проживання
    try:
        residence_field = driver.switch_to.active_element
        residence_field.send_keys("Смт. Любар")
    except Exception as e:
        print(f"Не вдалося ввести місце проживання: {e}")
        driver.quit()
        exit()

    residence_field.send_keys(Keys.TAB)

        # Введення номеру телефону
    try:
        phone_number_field = driver.switch_to.active_element
        phone_number_field.send_keys("0665760418")
    except Exception as e:
        print(f"Не вдалося ввести номер телефону: {e}")
        driver.quit()
        exit()

        # Використання TAB для переходу між полями ще 8 разів
    for _ in range(9):
        driver.switch_to.active_element.send_keys(Keys.TAB)
        time.sleep(0.1)

        # Натискання стрілочки вправо
    driver.switch_to.active_element.send_keys(Keys.ARROW_RIGHT)

        # Додаткові два натискання клавіші TAB
    for _ in range(2):
        driver.switch_to.active_element.send_keys(Keys.TAB)
        time.sleep(0.1)

        # Натискання пробіл
    driver.switch_to.active_element.send_keys(Keys.SPACE)

        # Натискання клавіші TAB
    driver.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(0.1)

        # Затримка в 5 секунд перед натисканням ENTER
    time.sleep(5)

        # Натискання ENTER
    driver.switch_to.active_element.send_keys(Keys.ENTER)

        # Затримка перед закриттям
    time.sleep(2)

        # Натискання на кнопку "Закрити"
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Закрити')]"))
        )
        close_button.click()
    except TimeoutException:
        print("Кнопка 'Закрити' не знайдена")
        driver.quit()
        exit()

    # Читання файлу кадастрових номерів
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
