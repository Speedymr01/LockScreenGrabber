'''**************************************************************************************************************************************************************************
This code should copy the windows spotlight lockscreen image and deliver it to a target folder
Version 2.3
**************************************************************************************************************************************************************************'''
import os
import shutil
from PIL import *
import logging
import cv2
import datetime
from datetime import *
import glob
import os.path
from funcs import ini_log, log_fini
import os

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"No working directory found. Directory created: {folder_path}")
        logging.info(f"No working directory found. Directory created: {folder_path}")
    else:
        print(f"Working Directory found: {folder_path}")
        logging.info(f"Working Directory found: {folder_path}")

def findimagespath():
    # Get the current user's home directory
    user_home = os.path.expanduser("~")
    
    # Construct the Packages path
    packages_path = os.path.join(user_home, "AppData", "Local", "Packages")
    
    # Use glob to find the correct path
    search_pattern = os.path.join(packages_path, "Microsoft.Windows.ContentDeliveryManager_*", "LocalState", "Assets")
    matching_paths = glob.glob(search_pattern)
    
    if matching_paths:
        path = matching_paths[0]  # Assuming the first match is the correct one
        path = path.replace('\\', '/')  # Swap backslashes to forward slashes
        path = f'{path}/'
        logging.info(f'Directory for images found: {path}')
        return path
    else:
        logging.error("ContentDeliveryManager path not found.")
        return None

# Log stuff
log_folder = "C:/Wallpaper_logs/"
create_folder_if_not_exists(log_folder)
script_log = ' Lockscreen Grabber'
Date_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
str_datetime = str(Date_time)
log_script_version_declaration = 'Initiated Windows loockscreen grabber v2.3'
logname = str(log_folder + str_datetime + script_log + ".log")
ini_log(logname)
logging.info(log_script_version_declaration)

folder = "C:/Wallpapers/"
create_folder_if_not_exists(folder)
file_path = folder
src_folder = findimagespath()
dst_folder = folder
dir_path = findimagespath()

def copy():
    coppied_files = 0
    not_coppied_files = 0
    total_files = 0
    for file_name in os.listdir(src_folder):
        source_copy = src_folder + file_name
        file_name = file_name + '.jpg'
        if file_name not in os.listdir(folder):
            dst_folder = folder + file_name
            copy_log_single = str('coping ' + file_name)
            logging.info(copy_log_single)
            shutil.copy(source_copy, dst_folder)
            coppied_files += 1
        else:
            not_coppied_files += 1
    total_files = not_coppied_files + coppied_files
    copy_log = str('copied ' + str(coppied_files) + ' files. Found ' + str(not_coppied_files) + ' reoccuring files. coppied ' + str(coppied_files) + ' out of ' + str(total_files) + '.')
    logging.info(copy_log)

def file_count():
    files = 0
    for path in os.scandir(file_path):
        if path.is_file():
            files = files + 1
    log_count_files = 'There are ' + str(files) + ' images in total.'
    logging.info(log_count_files)
    print(log_count_files)

def rename():
    errors = 0
    for file_name in os.listdir(folder):
        try:
            source = folder + file_name
            destination = source + '.jpg'
            os.rename(source, destination)
            log_rename = str('Sucsessfully renamed ' + source + ' to ' + destination)
            logging.info(log_rename)
        except PermissionError:
            error_text = str('The code encountered a permission error when renaming: ' + source)
            logging.info(error_text)
            errors = errors + 1
        except FileExistsError:
            error_text = str('The code encountered a File exists error when renaming: ' + source)
            logging.info(error_text)
            errors = errors + 1 
    if errors < 1:        
        logging.info('All files successfully re-named.')

def check_size():
    for filename in os.listdir(file_path):
        filename = file_path + filename
        size = os.path.getsize(filename)
        print(filename)
        if size < 100000:
            os.remove(filename)
            size_log = str(str(filename) + ' Deleted (icon)')
            print(size_log)
            logging.info(size_log)

def check_orientation():
    for filename in os.listdir(file_path):
        filename = file_path + filename
        im = cv2.imread(filename)
        h, w, c = im.shape
        if w < h:
            os.remove(filename)
            orientation_log = str(str(filename) + ' Deleted (portrait)')
            logging.info(orientation_log)
            print(filename, '    is portrait (Deleted)')
        else:
            print(filename, '    is landscape')
            orientation_landscape_log = filename + '      is landscape'
            logging.info(orientation_landscape_log)

copy()
check_size()
check_orientation()
file_count()
log_fini()