import os
import pandas as pd
import re

# Шляхи до файлів
folder_path = r"D:\Downloads"
new_registry_file = os.path.join(folder_path, "реєстр_кадастрових_номерів_за_датою.xlsx")

# Пошук файлу "обробка"
processing_file = None
for file_name in os.listdir(folder_path):
    if "обробка" in file_name.lower() and file_name.endswith(".xls"):
        processing_file = os.path.join(folder_path, file_name)
        break

if not processing_file:
    print("Файл 'обробка' не знайдено в папці.")
    exit()

# Завантаження реєстрів
new_registry_df = pd.read_excel(new_registry_file)
processing_df = pd.read_excel(processing_file)

# Перевірка колонок
print("\nКолонки реєстру 'реєстр_кадастрових_номерів_за_датою':")
print(new_registry_df.columns)

print("\nКолонки реєстру 'обробка':")
print(processing_df.columns)

# Пошук стовпчика з кадастровими номерами у "обробка"
cadastral_column = None
for col in processing_df.columns:
    # Перевіряємо, чи в колонці є хоча б один кадастровий номер
    if processing_df[col].astype(str).str.contains(r'\d{10}:\d{2}:\d{3}:\d{4}', na=False).any():
        cadastral_column = col
        print(f"\nКадастрові номери знайдено у колонці: {cadastral_column}")
        break

if cadastral_column is None:
    print("У реєстрі 'обробка' не знайдено колонку з кадастровими номерами.")
    exit()

# Об'єднання даних
# Робимо ліве об'єднання (left join), щоб зберегти всі дані з "обробка"
merged_df = processing_df.merge(
    new_registry_df[['Кадастровий номер', 'Грошова оцінка']],  # Залишаємо потрібні колонки з нового реєстру
    how='left',  # Ліве об'єднання
    left_on=cadastral_column,  # Колонка з кадастровими номерами у "обробка"
    right_on='Кадастровий номер'  # Колонка з кадастровими номерами у новому реєстрі
)

# Збереження оновленого реєстру
updated_processing_file = os.path.join(folder_path, "обробка_оновлена.xlsx")
merged_df.to_excel(updated_processing_file, index=False)

print(f"\nОновлений реєстр збережено: {updated_processing_file}")
