import re
import os
import requests
from PIL import Image
from skimage import io
import concurrent.futures
import shutil

# Constants string
from common.Constants import COMMON_DEBUG, images_ext

# Constants number
from common.Constants import max_length_idx, max_download_trial

# Constant object
from common.Constants import header_obj, timeout_obj, resource_cp_files

# Other constants
from common.Constants import using_thread, folder_running_resource, folder_sample_resource

# Messages
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_DOWN_IMG

from common.Validations import check_and_create_folder, check_file_exist

DEBUG_OBJ = {
    "is_image_file": True,
    "generate_filename": True,
    "extract_number": True,
    "resize_image": True,
    "check_image_error": True,
    "download_image": True,
    "execute_process": True,
}

def is_image_file(file_name=''):
    """
    Check if a file is an image file
    :param file_name: file name to check
    :return: True if the file is an image file, False otherwise
    """
    
    # Debug print initial
    if COMMON_DEBUG and DEBUG_OBJ["is_image_file"]:
        log_start_function("Common", "is_image_file")
        log_parameter("File name", file_name, 1)
    
    ext = file_name.split('.')[-1]
    
    result = ext in images_ext
    
    # Debug print result
    if COMMON_DEBUG and DEBUG_OBJ["is_image_file"]:
        log_parameter("Result", result, 2)
        print(END_LOG)

    return result

def generate_filename(prefix: str='', idx: int=0, ext: str='', str_len: int=max_length_idx):
    """
    Generate a filename with a specific format
    :param prefix: prefix of the filename
    :param idx: index of the filename
    :param ext: extension of the filename
    :param str_len: length of the index
    :return: a filename with the format: prefix + index + ext
    """

    # Debug print initial
    if COMMON_DEBUG and DEBUG_OBJ["generate_filename"]:
        log_start_function("Common", "generate_filename")
        log_parameter("Prefix", prefix, 1)
        log_parameter("Index", idx, 1)
        log_parameter("File extension", ext, 1)
        log_parameter("String length", str_len, 1)
    
    # Generate filename
    result_str = "0"*str_len + str(idx)
    result_str = result_str[-1*str_len:]
    result_str = f"{prefix}{result_str}{ext}"
    
    # Debug print result
    if COMMON_DEBUG and DEBUG_OBJ["generate_filename"]:
        log_parameter("Result str", result_str, 2)
        print(END_LOG)
    
    return result_str


def extract_number(s: str='', last: bool=False, is_float: bool=False):
    """
    Extract number from a string
    :param s: input string
    :param last: extract the last number
    :param is_float: extract the float number
    :return: a number extracted from the string
    """
    
    # Debug print initial
    if COMMON_DEBUG and DEBUG_OBJ["extract_number"]:
        log_start_function("Common", "extract_number")
        log_parameter("String", s, 1)
        log_parameter("Last", last, 1)
        log_parameter("Is float", is_float, 1)
    
    # Extract the last number in the string
    if last:
        if '.' in s:
            match = re.findall(r'\d+\.\d+', s)
        else:
            match = re.findall(r'\d+', s)
            
        result = match[-1]
        
        result = (float(result) if is_float else int(result)) if match else 0
        
        # Debug print result
        if COMMON_DEBUG and DEBUG_OBJ["extract_number"]:
            log_parameter("Result", result, 2)
            print(END_LOG)
        
        return result
        
    
    # Extract the first number in the string
    match = re.search(r'\d+', s)

    result = (float(match.group()) if is_float else int(match.group())) if match else 0
    
    result = float(result) if is_float else int(result)

    # Debug print result
    if COMMON_DEBUG and DEBUG_OBJ["extract_number"]:
        log_parameter("Result", result, 2)
        print(END_LOG)

    return result

def is_image_error(filename: str=''):
    """
    Check image error
    :param filename: filename to check
    :return: None
    """
    
    # Debug print initial
    if COMMON_DEBUG and DEBUG_OBJ["check_image_error"]:
        log_start_function("Common", "check_image_error")
        log_parameter("Filename", filename, 1)

    is_error = False
    try:
        img = Image.open(filename)  # open the image file
        img.verify()  # verify that it is, in fact an image
        img = io.imread(filename)
    except Exception as e:
        is_error = True
    
    if COMMON_DEBUG and DEBUG_OBJ["check_image_error"]:
        log_parameter("Is error", is_error, 2)
        print(END_LOG)

    return is_error
        
def download_image(link: str, server: str, file: str):
    """
    Download image from link
    :param link: link to download
    :param server: server to download
    :param file: file to save
    :return: return status code
    """
    
    # Debug print initial
    if COMMON_DEBUG and DEBUG_OBJ["download_image"]:
        log_start_function("Common", "download_image")
        log_parameter("Link", link, 1)
        log_parameter("Server", server, 1)
        log_parameter("File", file, 1)

    if os.path.exists(file) and not is_image_error(file):
        return 200

    req_headers = {
        **header_obj,
        'Referer': server,
    }

    download_success = False
    for i in range(max_download_trial):
        try:
            r = requests.get(link, headers=req_headers, timeout=timeout_obj)
            
            with open(file, "wb") as fd:
                down_code = r.status_code
                if COMMON_DEBUG and DEBUG_OBJ["download_image"]:
                    log_parameter("Down code", down_code, 2)
                if down_code != 200:
                    raise Exception(f"Error download image {link}")
                else:
                    fd.write(r.content)
            
            if not is_image_error(file):
                download_success = True
                break
            
            return 200
            
        except Exception as e:
            if COMMON_DEBUG and DEBUG_OBJ["download_image"]:
                log_error("Common", "download_image", MSG_ERR_DOWN_IMG.format(i), False)
            continue

    result = 200 if download_success else 400

    if COMMON_DEBUG and DEBUG_OBJ["download_image"]:
        log_parameter("Result", result, 2)
        print(END_LOG)

    return result

def execute_process(func, obj_list):
    """
    Execute process with multithreading if supported
    :param func: function to execute
    :param obj_list: list of objects to execute
    :return: None
    """
    if using_thread:
        thread_count = os.cpu_count() // 2 if os.cpu_count() > 1 else 1
        COMMON_DEBUG and DEBUG_OBJ["execute_process"] and log_parameter("Thread count", thread_count, 2)
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
            executor.map(func, obj_list)
    else:
        for obj in obj_list:
            func(obj)

def init_app():
    """
    Initial function for running app
    :return: None
    """
    check_and_create_folder(folder_running_resource)
    
    for file in resource_cp_files:
        check_file_exist(os.path.join(folder_sample_resource, file))
        if not os.path.exists(os.path.join(folder_running_resource, file)):
            shutil.copy(os.path.join(folder_sample_resource, file), os.path.join(folder_running_resource, file))
