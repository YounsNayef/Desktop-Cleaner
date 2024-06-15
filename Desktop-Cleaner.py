import os
import shutil
import logging
from typing import Dict

def setup_logging(log_file):
    """Set up logging configuration"""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def get_folders():
    """Get folders and their corresponding file extensions"""
    return {
        "Documents": [".txt", ".doc", ".docx", ".pdf"],
        "Images": [".jpg", ".png", ".gif", ".bmp"],
        "Videos": [".mp4", ".avi", ".mov"],
        "Music": [".mp3", ".wav", ".flac"],
        "Others": []  # Default folder for files with unknown extensions
    }

def move_file(file_path, destination_folder):
    """Move file to destination folder"""
    try:
        shutil.move(file_path, destination_folder)
        logging.info(f"Moved '{file_path}' to '{destination_folder}'")
    except Exception as e:
        logging.error(f"Failed to move '{file_path}' to '{destination_folder}': {e}")

def clean_desktop(desktop_path, custom_folders: Dict[str, list] = None):
    """Organize files on desktop into folders based on their extensions"""
    folders = custom_folders if custom_folders else get_folders()

    for folder_name in folders:
        folder_path = os.path.join(desktop_path, folder_name)
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                logging.info(f"Created folder '{folder_path}'")
            except Exception as e:
                logging.error(f"Failed to create folder '{folder_path}': {e}")

    for filename in os.listdir(desktop_path):
        if filename != "desktop_cleaner.py":  # Exclude the script file itself
            file_path = os.path.join(desktop_path, filename)
            if os.path.isfile(file_path):
                _, extension = os.path.splitext(filename)
                extension = extension.lower()

                found = False
                for folder_name, extensions in folders.items():
                    if extension in extensions:
                        destination_folder = os.path.join(desktop_path, folder_name)
                        move_file(file_path, destination_folder)
                        found = True
                        break

                if not found:
                    destination_folder = os.path.join(desktop_path, "Others")
                    move_file(file_path, destination_folder)

    print("Your desktop has been tidied up!")

if __name__ == "__main__":
    desktop_path = os.path.expanduser("~/Desktop")
    log_file = os.path.join(desktop_path, "desktop_cleaner.log")
    setup_logging(log_file)

    try:
        custom_folders = {
            "Programming": [".py", ".java", ".c", ".cpp"],
            "Spreadsheets": [".xls", ".xlsx", ".csv"],
            "Compressed": [".zip", ".rar", ".7z"],
        }
        clean_desktop(desktop_path, custom_folders)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
