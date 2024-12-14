import re
import os
import requests
from PIL import Image
from skimage import io
from lxml import html
from colorama import Fore, Style

from common.Constants import COMMON_DEBUG

# constants number
from common.Constants import max_length_idx, max_download_trial

# constants objects
from common.Constants import header_obj


DEBUG_OBJ = {
    "is_image_file": False,
    "generate_filename": False,
    "extract_number": False,
    "resize_image": True,
    "check_image_error": False,
    "download_image": True,
}

def is_image_file(file_name=''):
    """
    Check if a file is an image file
    :param file_name: file name to check
    :return: True if the file is an image file, False otherwise
    """
    
    # Debug print initial
    if COMMON_DEBUG and DEBUG_OBJ["is_image_file"]:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Common: is_image_file'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"File name:":<20}' + Style.RESET_ALL + f'{file_name: >49}')
    
    ext = file_name.split('.')[-1]
    
    result = ext in ['jpg', 'png', 'jpeg']
    
    # Debug print result
    if COMMON_DEBUG and DEBUG_OBJ["is_image_file"]:
        print(Fore.CYAN + f'{"Result:":<20}' + Style.RESET_ALL + f'{str(result): >49}')
        print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

    return result

def generate_filename(prefix='', idx=0, ext='', str_len=max_length_idx):
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
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Common: generate_filename'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"Prefix:":<20}' + Style.RESET_ALL + f'{prefix: >49}')
        print(Fore.BLUE + f'{"Index:":<20}' + Style.RESET_ALL + f'{idx: >49}')
        print(Fore.BLUE + f'{"Ext:":<20}' + Style.RESET_ALL + f'{ext: >49}')
        print(Fore.BLUE + f'{"Str len:":<20}' + Style.RESET_ALL + f'{str_len: >49}')
    
    # Generate filename
    result_str = "0"*str_len + str(idx)
    result_str = result_str[-1*str_len:]
    result_str = f"{prefix}{result_str}{ext}"
    
    # Debug print result
    if COMMON_DEBUG and DEBUG_OBJ["generate_filename"]:
        print(Fore.CYAN + f'{"Result str:":<20}' + Style.RESET_ALL + f'{result_str: >49}')
        print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
    
    return result_str


def extract_number(s='', last=False, is_float=False):
    """
    Extract number from a string
    :param s: input string
    :param last: extract the last number
    :param is_float: extract the float number
    :return: a number extracted from the string
    """
    
    # Debug print initial
    if COMMON_DEBUG and DEBUG_OBJ["extract_number"]:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Common: extract_number'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"String:":<20}' + Style.RESET_ALL + f'{s: >49}')
        print(Fore.BLUE + f'{"Last:":<20}' + Style.RESET_ALL + f'{last: >49}')
        print(Fore.BLUE + f'{"Is float:":<20}' + Style.RESET_ALL + f'{is_float: >49}')
    
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
            print(Fore.CYAN + f'{"Result:":<20}' + Style.RESET_ALL + f'{result: >49}')
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
        
        return result
        
    
    # Extract the first number in the string
    match = re.search(r'\d+', s)

    result = (float(match.group()) if is_float else int(match.group())) if match else 0
    
    result = float(result) if is_float else int(result)

    # Debug print result
    if COMMON_DEBUG and DEBUG_OBJ["extract_number"]:
        print(Fore.CYAN + f'{"Result:":<20}' + Style.RESET_ALL + f'{result: >49}')
        print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

    return result

def is_image_error(filename=''):
    """
    Check image error
    :param filename: filename to check
    :return: None
    """
    
    # Debug print initial
    if COMMON_DEBUG and DEBUG_OBJ["check_image_error"]:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Common: check_image_error'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"Filename:":<20}' + Style.RESET_ALL + f'{filename: >49}')

    is_error = False
    try:
        img = Image.open(filename)  # open the image file
        img.verify()  # verify that it is, in fact an image
        img = io.imread(filename)
    except Exception as e:
        if COMMON_DEBUG and DEBUG_OBJ["check_image_error"]:
            print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{e: >49}')
        is_error = True
    
    if COMMON_DEBUG and DEBUG_OBJ["check_image_error"]:
        print(Fore.CYAN + f'{"Result is_error:":<20}' + Style.RESET_ALL + f'{str(is_error): >49}')
        print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
        
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
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Common: download_image'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"Link:":<20}' + Style.RESET_ALL + f'{link: >49}')
        print(Fore.BLUE + f'{"Server:":<20}' + Style.RESET_ALL + f'{server: >49}')
        print(Fore.BLUE + f'{"File:":<20}' + Style.RESET_ALL + f'{file: >49}')

    if os.path.exists(file) and not is_image_error(file):
        return 200

    download_success = False
    for i in range(max_download_trial):
        try:
            r = requests.get(link, headers={
                'User-agent': 'Mozilla/5.0', 'Referer': server}, timeout=(3, 5))
            
            with open(file, "wb") as fd:
                down_code = r.status_code
                COMMON_DEBUG and DEBUG_OBJ["download_image"] and print(Fore.CYAN + f'{"Down code:":<20}' + Style.RESET_ALL + f'{down_code: >49}')
                if down_code != 200:
                    raise Exception(f"Error download image {link}")
                else:
                    fd.write(r.content)
            
            if not is_image_error(file):
                download_success = True
                break
            
            return 200
            
        except Exception as e:
            COMMON_DEBUG and DEBUG_OBJ["download_image"] and print(Fore.RED + f'{"Error at trial:":<20}' + Style.RESET_ALL + f'{i: >49}')
            continue

    result = 200 if download_success else 400

    if COMMON_DEBUG and DEBUG_OBJ["download_image"]:
        print(Fore.CYAN + f'{"Result:":<20}' + Style.RESET_ALL + f'{result: >49}')
        print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

    return result
