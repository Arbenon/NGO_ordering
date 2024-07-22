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

chrome_options = Options()
chrome_options.add_argument("user-data-dir=/home/arbenon/.config/google-chrome")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    driver.get("https://e.land.gov.ua/back/service/main")

    time.sleep(10)

    try:
        info_DZK_link = WebDriverWait(driver, 0.1).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Відомості ДЗК')]"))
        )
    except TimeoutException:
        try:
            info_DZK_link = WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Відомості ДЗК"))
            )
        except TimeoutException:
            try:
                info_DZK_link = WebDriverWait(driver, 0.1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='Відомості ДЗК']"))
                )
            except TimeoutException:
                driver.quit()
                exit()

    if info_DZK_link:
        info_DZK_link.click()

    try:
        info_DZK_order_link = WebDriverWait(driver, 0.1).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Замовити')]"))
        )
    except TimeoutException:
        try:
            info_DZK_order_link = WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Замовити"))
            )
        except TimeoutException:
            try:
                info_DZK_order_link = WebDriverWait(driver, 0.1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='Замовити']"))
                )
            except TimeoutException:
                driver.quit()
                exit()

    if info_DZK_order_link:
        info_DZK_order_link.click()

    time.sleep(1)

    try:
        application_type_dropdown = WebDriverWait(driver, 0.1).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Тип заяви')]/following-sibling::select"))
        )
        application_type_dropdown.click()

        for _ in range(6):
            application_type_dropdown.send_keys(Keys.ARROW_DOWN)
        application_type_dropdown.send_keys(Keys.ENTER)
        
    except TimeoutException:
        driver.quit()
        exit()

    time.sleep(0.1)

    try:
        cadastral_number_field = WebDriverWait(driver, 0.1).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Кадастровий номер земельної ділянки')]/following-sibling::input"))
        )
        cadastral_number_field.send_keys("1825884400:02:000:0024")
    except TimeoutException:
        driver.quit()
        exit()

    time.sleep(2)

    # Використання TAB для переходу між полями
    for _ in range(9):
        driver.switch_to.active_element.send_keys(Keys.TAB)
        time.sleep(0.1)  # Додатковий час для уникнення пропусків полів

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
        time.sleep(0.1)  # Додатковий час для уникнення пропусків полів

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

finally:
    # Закриття браузера
    driver.quit()
