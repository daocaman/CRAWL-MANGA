import os
import json
from colorama import Fore, Style
from pprint import pprint

from common.Constants import LIST_AND_RENAME_DEBUG, rename_list_file

DEBUG_OBJ = {
    "get_list_of_files": LIST_AND_RENAME_DEBUG,
    "rename_file": LIST_AND_RENAME_DEBUG,
}

def get_list_of_files(path):
    """
    Get list of files in the given path and save to a JSON file.
    :param path: The path to get the list of files.
    :return: None
    """
    if LIST_AND_RENAME_DEBUG and DEBUG_OBJ["get_list_of_files"]:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'ListAndRenameController: get_list_of_files'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"Path:":<20}' + Style.RESET_ALL + f'{path: >49}')

    files = [f.encode('utf-8').decode('utf-8') for f in os.listdir(path)]
    file_objs = []
    for file in files:
        file_obj = {
            "root_path": path,
            "current_file_name": file,
            "new_file_name": file,
        }
        file_objs.append(file_obj)
        
    if LIST_AND_RENAME_DEBUG and DEBUG_OBJ["get_list_of_files"]:
        print(Fore.BLUE + f'{"File objects:":<20}' + Style.RESET_ALL)
        pprint(file_objs)
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
    
    with open(rename_list_file, "w+", encoding="utf-8") as f:
        json.dump(file_objs, f, indent=2, ensure_ascii=False)
        
def rename_file():
    """
    Rename the file with the given filename.
    :return: None
    """
    
    if LIST_AND_RENAME_DEBUG and DEBUG_OBJ["rename_file"]:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'ListAndRenameController: rename_file'.center(70) + Style.RESET_ALL)

    if not os.path.exists(rename_list_file):
        print(Fore.RED + f'{"File not found:":<20}' + Style.RESET_ALL + f'{rename_list_file: >49}')
        return
    
    with open(rename_list_file, "r", encoding="utf-8") as f:
        file_objs = json.load(f)
        
    for file_obj in file_objs:
        os.rename(os.path.join(file_obj["root_path"], file_obj["current_file_name"]), os.path.join(file_obj["root_path"], file_obj["new_file_name"]))
        
    LIST_AND_RENAME_DEBUG and DEBUG_OBJ["rename_file"] and print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
    