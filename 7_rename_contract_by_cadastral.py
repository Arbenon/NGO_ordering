import os
import re
from docx import Document

# Define the root directory where DOCX files are stored
root_dir = r"D:\Downloads\TEMPORARY"

# Regular expression to find the cadastral number pattern (e.g., 1825880500:02:000:0287)
cad_pattern = re.compile(r"\b\d{10}:\d{2}:\d{3}:\d{4}\b")

def extract_cadastral_number(docx_path):
    """Extracts cadastral number from the text of a DOCX file."""
    try:
        doc = Document(docx_path)
        for paragraph in doc.paragraphs:
            match = cad_pattern.search(paragraph.text)
            if match:
                return match.group().replace(":", " ")  # Replace colons with spaces
    except Exception as e:
        print(f"Error reading {docx_path}: {e}")
    return None

def get_unique_filename(folder, base_name):
    """Ensures the new filename is unique by adding (1), (2), etc., if needed."""
    new_name = f"{base_name}.docx"
    new_path = os.path.join(folder, new_name)
    
    counter = 1
    while os.path.exists(new_path):
        new_name = f"{base_name}({counter}).docx"
        new_path = os.path.join(folder, new_name)
        counter += 1
    
    return new_path

def rename_docx_files(root_directory):
    """Finds and renames DOCX files in all subfolders."""
    for foldername, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.lower().endswith(".docx"):
                docx_path = os.path.join(foldername, filename)
                cadastral_number = extract_cadastral_number(docx_path)

                if cadastral_number:
                    unique_path = get_unique_filename(foldername, cadastral_number)
                    os.rename(docx_path, unique_path)
                    print(f"Renamed: {filename} → {os.path.basename(unique_path)}")
                else:
                    print(f"No cadastral number found in {filename}")

if __name__ == "__main__":
    rename_docx_files(root_dir)