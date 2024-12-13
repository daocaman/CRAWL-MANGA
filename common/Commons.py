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
    COMMON_DEBUG and DEBUG_OBJ["is_image_file"] and print("="*50)
    COMMON_DEBUG and DEBUG_OBJ["is_image_file"] and print('Common: is_image_file')
    COMMON_DEBUG and DEBUG_OBJ["is_image_file"] and print(f"File name: {file_name}")
    
    ext = file_name.split('.')[-1]
    
    result = ext in ['jpg', 'png', 'jpeg']
    
    # Debug print result
    COMMON_DEBUG and DEBUG_OBJ["is_image_file"] and print(f"Result: {result}")
    COMMON_DEBUG and DEBUG_OBJ["is_image_file"] and print("="*50)

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
    COMMON_DEBUG and DEBUG_OBJ["generate_filename"] and print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
    COMMON_DEBUG and DEBUG_OBJ["generate_filename"] and print(Fore.YELLOW + 'Common: generate_filename'.center(70) + Style.RESET_ALL)
    COMMON_DEBUG and DEBUG_OBJ["generate_filename"] and print(Fore.BLUE + f'{"Prefix:":<20}' + Style.RESET_ALL + f'{prefix: >49}')
    COMMON_DEBUG and DEBUG_OBJ["generate_filename"] and print(Fore.BLUE + f'{"Index:":<20}' + Style.RESET_ALL + f'{idx: >49}')
    COMMON_DEBUG and DEBUG_OBJ["generate_filename"] and print(Fore.BLUE + f'{"Ext:":<20}' + Style.RESET_ALL + f'{ext: >49}')
    COMMON_DEBUG and DEBUG_OBJ["generate_filename"] and print(Fore.BLUE + f'{"Str len:":<20}' + Style.RESET_ALL + f'{str_len: >49}')
    
    # Generate filename
    result_str = "0"*str_len + str(idx)
    result_str = result_str[-1*str_len:]
    result_str = f"{prefix}{result_str}{ext}"
    
    # Debug print result
    COMMON_DEBUG and DEBUG_OBJ["generate_filename"] and print(Fore.CYAN + f'{"Result str:":<20}' + Style.RESET_ALL + f'{result_str: >49}')
    COMMON_DEBUG and DEBUG_OBJ["generate_filename"] and print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
    
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
    COMMON_DEBUG and DEBUG_OBJ["extract_number"] and print("="*50)
    COMMON_DEBUG and DEBUG_OBJ["extract_number"] and print('Common: extract_number')
    COMMON_DEBUG and DEBUG_OBJ["extract_number"] and print(f"String: {s}\nLast: {last}\nIs float: {is_float}")
    
    # Extract the last number in the string
    if last:
        if '.' in s:
            match = re.findall(r'\d+\.\d+', s)
        else:
            match = re.findall(r'\d+', s)
            
        result = match[-1]
        
        result = (float(result) if is_float else int(result)) if match else 0
        
        # Debug print result
        COMMON_DEBUG and DEBUG_OBJ["extract_number"] and print(f"Result: {result}")
        COMMON_DEBUG and DEBUG_OBJ["extract_number"] and print("="*50)
        
        return result
        
    
    # Extract the first number in the string
    match = re.search(r'\d+', s)

    result = (float(match.group()) if is_float else int(match.group())) if match else 0
    
    result = float(result) if is_float else int(result)

    # Debug print result
    COMMON_DEBUG and DEBUG_OBJ["extract_number"] and print(f"Result: {result}")
    COMMON_DEBUG and DEBUG_OBJ["extract_number"] and print("="*50)

    return result

def is_image_error(filename=''):
    """
    Check image error
    :param filename: filename to check
    :return: None
    """
    
    # Debug print initial
    COMMON_DEBUG and DEBUG_OBJ["check_image_error"] and print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
    COMMON_DEBUG and DEBUG_OBJ["check_image_error"] and print(Fore.YELLOW + 'Common: check_image_error'.center(70) + Style.RESET_ALL)
    COMMON_DEBUG and DEBUG_OBJ["check_image_error"] and print(Fore.BLUE + f'{"Filename:":<20}' + Style.RESET_ALL + f'{filename: >49}')

    is_error = False
    try:
        img = Image.open(filename)  # open the image file
        img.verify()  # verify that it is, in fact an image
        img = io.imread(filename)
    except Exception as e:
        COMMON_DEBUG and DEBUG_OBJ["check_image_error"] and print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{e: >49}')
        is_error = True
    
    COMMON_DEBUG and DEBUG_OBJ["check_image_error"] and print(Fore.CYAN + f'{"Result is_error:":<20}' + Style.RESET_ALL + f'{str(is_error): >49}')
    
    COMMON_DEBUG and DEBUG_OBJ["check_image_error"] and print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
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
    COMMON_DEBUG and DEBUG_OBJ["download_image"] and print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
    COMMON_DEBUG and DEBUG_OBJ["download_image"] and print(Fore.YELLOW + 'Common: download_image'.center(70) + Style.RESET_ALL)
    COMMON_DEBUG and DEBUG_OBJ["download_image"] and print(Fore.BLUE + f'{"Link:":<20}' + Style.RESET_ALL + f'{link: >49}')
    COMMON_DEBUG and DEBUG_OBJ["download_image"] and print(Fore.BLUE + f'{"Server:":<20}' + Style.RESET_ALL + f'{server: >49}')
    COMMON_DEBUG and DEBUG_OBJ["download_image"] and print(Fore.BLUE + f'{"File:":<20}' + Style.RESET_ALL + f'{file: >49}')

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

    COMMON_DEBUG and DEBUG_OBJ["download_image"] and print(Fore.CYAN + f'{"Result:":<20}' + Style.RESET_ALL + f'{result: >49}')
    COMMON_DEBUG and DEBUG_OBJ["download_image"] and print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

    return result

def get_info_chapter(link: str, xpath: str, is_list = True, list_item_ele = ''):
    """
    Get information from chapter
    :param link: link to get information
    :param xpath: xpath to get information
    :param is_list: is list of information
    :param list_item_ele: list item element
    :return: information
    """
    
    # Debug print initial
    COMMON_DEBUG and DEBUG_OBJ["get_info_chapter"] and print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
    COMMON_DEBUG and DEBUG_OBJ["get_info_chapter"] and print(Fore.YELLOW + 'Common: get_info_chapter'.center(70) + Style.RESET_ALL)
    COMMON_DEBUG and DEBUG_OBJ["get_info_chapter"] and print(Fore.BLUE + f'{"Link:":<20}' + Style.RESET_ALL + f'{link: >49}')
    COMMON_DEBUG and DEBUG_OBJ["get_info_chapter"] and print(Fore.BLUE + f'{"Xpath:":<20}' + Style.RESET_ALL + f'{xpath: >49}')
    COMMON_DEBUG and DEBUG_OBJ["get_info_chapter"] and print(Fore.BLUE + f'{"Is list:":<20}' + Style.RESET_ALL + f'{str(is_list): >49}')
    COMMON_DEBUG and DEBUG_OBJ["get_info_chapter"] and print(Fore.BLUE + f'{"List item ele:":<20}' + Style.RESET_ALL + f'{list_item_ele: >49}')

    r = requests.get(link, headers=header_obj, timeout=(3, 5))
    tree = html.fromstring(r.content)

    COMMON_DEBUG and DEBUG_OBJ["get_info_chapter"] and print(f"Tree: {tree.xpath(xpath)}")

    if not is_list:
        COMMON_DEBUG and DEBUG_OBJ["get_info_chapter"] and print(f"Tree: {tree.xpath(xpath+'/text()')}")
        return tree.xpath(xpath+"/text()")
    else:
        chapters = tree.xpath(xpath + f"//{list_item_ele}")

        # get text from each element in the list
        for chap in chapters:
            tmp_text = chap.xpath(".//text()")
            tmp_text = "".join(tmp_text)
            if tmp_text != "":
                COMMON_DEBUG and DEBUG_OBJ["get_info_chapter"] and print(f"Tmp text: {tmp_text}")

    # Debug print final
    COMMON_DEBUG and DEBUG_OBJ["get_info_chapter"] and print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

    return chapters
