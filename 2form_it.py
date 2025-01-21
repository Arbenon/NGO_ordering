import os
import pandas as pd
import fitz  # PyMuPDF для роботи з PDF
from datetime import datetime

# Шлях до папки
folder_path = r"D:\Downloads"

# Функція для витягування даних із PDF
def extract_data_from_pdf(file_path):
    try:
        # Відкриваємо PDF
        pdf_document = fitz.open(file_path)
        text = ""
        for page in pdf_document:  # Читаємо всі сторінки
            text += page.get_text()
        pdf_document.close()
        
        # Виводимо текст для діагностики
        print(f"\nТекст із файлу {file_path}:\n{text}\n")

        # Шукаємо кадастровий номер та грошову оцінку
        cadastral_number = None
        monetary_value = None

        lines = text.splitlines()  # Розбиваємо текст на рядки
        for i, line in enumerate(lines):
            # Шукаємо кадастровий номер
            if ":" in line and len(line.split(":")) == 4:  # Формат кадастрового номера
                cadastral_number = line.strip()
                print(f"Знайдено кадастровий номер: {cadastral_number}")
                # Перевіряємо, чи є наступний рядок
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line.replace(".", "").isdigit():  # Якщо це число
                        monetary_value = next_line
                        print(f"Знайдено грошову оцінку: {monetary_value}")
        
        return cadastral_number, monetary_value
    except Exception as e:
        print(f"Помилка обробки файлу {file_path}: {e}")
        return None, None

# Збираємо інформацію про файли
file_data = []
for file_name in os.listdir(folder_path):
    if file_name.endswith(".pdf"):
        full_path = os.path.join(folder_path, file_name)
        
        # Отримуємо час створення файлу
        creation_time = os.path.getctime(full_path)  # UNIX-мітка часу
        creation_time_formatted = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        
        # Витягуємо кадастровий номер та грошову оцінку
        cadastral_number, monetary_value = extract_data_from_pdf(full_path)
        if cadastral_number and monetary_value:  # Якщо знайдені обидва значення
            file_data.append({
                "Назва файлу": file_name,
                "Кадастровий номер": cadastral_number,
                "Грошова оцінка": monetary_value,
                "Дата створення файлу": creation_time_formatted
            })

# Перевіряємо, чи є знайдені файли
if file_data:
    # Створюємо DataFrame
    df = pd.DataFrame(file_data)
    
    # Сортуємо за датою створення файлу (від новіших до старіших)
    df = df.sort_values(by="Дата створення файлу", ascending=False)

    # Зберігаємо у файл Excel
    output_file = os.path.join(folder_path, "реєстр_кадастрових_номерів_за_датою.xlsx")
    df.to_excel(output_file, index=False)

    print(f"Реєстр створено: {output_file}")
else:
    print("Не вдалося знайти кадастрові номери та грошові оцінки у файлах.")
