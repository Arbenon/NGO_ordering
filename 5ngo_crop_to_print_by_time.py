import os
import fitz  # PyMuPDF
from PIL import Image
import logging
import shutil  # Для видалення папок

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pdf_to_images.log"),
        logging.StreamHandler()
    ]
)

def get_sorted_files(folder, extension):
    """Повертає список файлів із заданим розширенням, відсортованих за часом останньої зміни."""
    files = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(extension)]
    files.sort(key=lambda x: os.path.getmtime(x))  # Сортування за часом останньої зміни
    return files

def pdf_to_images(input_folder, output_folder, dpi=300):
    """Конвертує PDF у зображення за порядком останньої зміни файлів."""
    os.makedirs(output_folder, exist_ok=True)
    pdf_files = get_sorted_files(input_folder, ".pdf")  # Сортуємо PDF-файли за часом останньої зміни
    for file in pdf_files:
        pdf_name = os.path.splitext(os.path.basename(file))[0]
        try:
            pdf_document = fitz.open(file)
            logging.info(f"Конвертуємо файл {file} у зображення...")
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                pix = page.get_pixmap(dpi=dpi)
                image_path = os.path.join(output_folder, f"{pdf_name}_page_{page_num + 1}.png")
                pix.save(image_path)
                logging.info(f"Сторінка {page_num + 1} збережена як {image_path}")
            pdf_document.close()
        except Exception as e:
            logging.error(f"Помилка під час конвертації {file}: {e}")

def crop_images(input_folder, output_folder, crop_box_top, crop_box_bottom):
    """Обрізає верхню та нижню частини зображень за порядком останньої зміни."""
    os.makedirs(output_folder, exist_ok=True)
    image_files = get_sorted_files(input_folder, ".png")  # Сортуємо зображення за часом останньої зміни
    for file in image_files:
        output_path = os.path.join(output_folder, f"merged_{os.path.basename(file)}")
        try:
            img = Image.open(file)
            width, height = img.size
            cropped_top = img.crop(crop_box_top)
            crop_box_bottom_actual = (0, height - crop_box_bottom[3], crop_box_bottom[2], height)
            cropped_bottom = img.crop(crop_box_bottom_actual)
            merged_height = cropped_top.height + cropped_bottom.height
            merged_img = Image.new("RGB", (width, merged_height))
            merged_img.paste(cropped_top, (0, 0))
            merged_img.paste(cropped_bottom, (0, cropped_top.height))
            merged_img.save(output_path)
            logging.info(f"Збережено об'єднане зображення як {output_path}")
        except Exception as e:
            logging.error(f"Помилка під час обрізання {file}: {e}")

def combine_all_images_to_pdf(input_folder, output_file):
    """Об'єднує всі зображення в один PDF у порядку за часом останньої зміни."""
    image_files = get_sorted_files(input_folder, ".png")  # Сортуємо за часом останньої зміни
    if not image_files:
        logging.warning("У папці немає зображень для об'єднання.")
        return
    try:
        images = []
        for file in image_files:
            img = Image.open(file)
            if img.mode != "RGB":
                img = img.convert("RGB")
            images.append(img)
        images[0].save(output_file, save_all=True, append_images=images[1:])
        logging.info(f"PDF створено та збережено у {output_file}")
    except Exception as e:
        logging.error(f"Помилка під час створення PDF: {e}")

def clean_up_folders(folders):
    """Видаляє тимчасові папки."""
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

crop_box_top = (0, 0, 2500, 1300)
crop_box_bottom = (0, 0, 2500, 800)

# 1. Конвертація PDF у зображення
pdf_to_images(pdf_folder, images_folder)

# 2. Обрізка зображень
crop_images(images_folder, cropped_images_folder, crop_box_top, crop_box_bottom)

# 3. Об'єднання всіх зображень у PDF
combine_all_images_to_pdf(cropped_images_folder, final_pdf_file)

# 4. Видалення тимчасових папок
clean_up_folders([images_folder, cropped_images_folder])
