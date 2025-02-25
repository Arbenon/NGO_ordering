import os
import fitz  # PyMuPDF
from PIL import Image
import logging  # Додано імпорт
import re
import locale
import win32file

def get_creation_time(file):
    return win32file.GetFileTime(win32file.CreateFile(
        file, 0x80, 0x01, None, 3, 0x02000000, None))[0]

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pdf_to_images.log"),
        logging.StreamHandler()
    ]
)

def pdf_to_images(input_folder, output_folder, dpi=300):
    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(input_folder):
        if file.endswith(".pdf"):
            input_path = os.path.join(input_folder, file)
            pdf_name = os.path.splitext(file)[0]
            try:
                # Відкриваємо PDF
                pdf_document = fitz.open(input_path)
                logging.info(f"Конвертуємо файл {file} у зображення...")
                
                for page_num in range(len(pdf_document)):
                    # Конвертуємо сторінку у зображення
                    page = pdf_document[page_num]
                    pix = page.get_pixmap(dpi=dpi)  # Висока роздільна здатність
                    image_path = os.path.join(output_folder, f"{pdf_name}_page_{page_num + 1}.png")
                    pix.save(image_path)
                    logging.info(f"Сторінка {page_num + 1} збережена як {image_path}")

                pdf_document.close()
            except Exception as e:
                logging.error(f"Помилка під час конвертації {file}: {e}")

def crop_images(input_folder, output_folder, crop_box_top, crop_box_bottom):
    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(input_folder):
        if file.endswith(".png"):
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, f"merged_{file}")
            try:
                # Відкриваємо зображення
                img = Image.open(input_path)
                width, height = img.size

                # Обрізаємо верхню частину
                cropped_top = img.crop(crop_box_top)
                logging.info(f"Верхня частина {file} обрізана")

                # Обчислюємо координати для нижньої частини
                crop_box_bottom_actual = (0, height - crop_box_bottom[3], crop_box_bottom[2], height)
                cropped_bottom = img.crop(crop_box_bottom_actual)
                logging.info(f"Нижня частина {file} обрізана")

                # Створюємо нове зображення для об'єднання
                merged_height = cropped_top.height + cropped_bottom.height
                merged_img = Image.new("RGB", (width, merged_height))

                # Додаємо верхню і нижню частини
                merged_img.paste(cropped_top, (0, 0))
                merged_img.paste(cropped_bottom, (0, cropped_top.height))
                logging.info(f"Верх і низ {file} об'єднано")

                # Зберігаємо з'єднане зображення
                merged_img.save(output_path)
                logging.info(f"Збережено об'єднане зображення як {output_path}")
            except Exception as e:
                logging.error(f"Помилка під час обробки {file}: {e}")

def combine_all_images_to_pdf(input_folder, output_file):
    # Отримуємо список файлів у папці
    files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith(".png")]
    
    # Сортуємо файли за датою створення
    #files.sort(key=lambda x: os.path.getctime(x))  # Сортування за часом створення
    #files.sort(key=lambda x: os.path.getmtime(os.path.join(input_folder, x)))
    

    #files.sort() #звичайне сортування за алфавітом
    #files.sort(key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group()))

    #ОКРЕМА ОПЦІЯ З ДВОХ РЯДКІВ
    locale.setlocale(locale.LC_COLLATE, "uk_UA.UTF-8")  # Встановлюємо українську локаль
    files.sort(key=locale.strxfrm)  # Сортуємо за українським алфавітом


    if not files:
        logging.warning("У папці немає зображень для об'єднання.")
        return

    try:
        # Відкриваємо всі зображення
        images = []
        for file in files:
            img = Image.open(file)
            if img.mode != "RGB":
                img = img.convert("RGB")  # Конвертуємо у формат RGB
            images.append(img)

        # Створюємо PDF із усіма зображеннями
        images[0].save(output_file, save_all=True, append_images=images[1:])
        logging.info(f"PDF створено та збережено у {output_file}")
    except Exception as e:
        logging.error(f"Помилка під час створення PDF: {e}")


import shutil  # Для видалення папок

# Видалення папок
def clean_up_folders(folders):
    for folder in folders:
        try:
            shutil.rmtree(folder)
            logging.info(f"Папка {folder} успішно видалена.")
        except Exception as e:
            logging.error(f"Помилка під час видалення папки {folder}: {e}")

# Параметри
pdf_folder = r"D:\Downloads"
images_folder = r"D:\Downloads\pdf_images"
cropped_images_folder = r"D:\Downloads\cropped_images"
final_pdf_file = r"D:\Downloads\final_output.pdf"

crop_box_top = (0, 0, 2500, 1300)  # Верхня область
crop_box_bottom = (0, 0, 2500, 800)  # Нижня область

# Конвертація PDF у зображення
pdf_to_images(pdf_folder, images_folder)

# Обрізка верхньої та нижньої частини і з'єднання
crop_images(images_folder, cropped_images_folder, crop_box_top, crop_box_bottom)

# Об'єднання всіх зображень у PDF
combine_all_images_to_pdf(cropped_images_folder, final_pdf_file)

# Видалення тимчасових папок
clean_up_folders([images_folder, cropped_images_folder])
