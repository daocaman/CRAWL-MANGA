import questionary
from art import art
from colorama import Fore, Style
import os

from common.Constant_v1_1 import radio_menu, error_message
from tasks.RenameFiles import main_process

def quest_form_rename_files():
    
    while True:
        ques_target_folder = f"Enter target folder: {art('gimme')}"
        target_folder = questionary.text(ques_target_folder).ask()
        
        if target_folder == "":
            print(Fore.RED + error_message["folder"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        
        if not os.path.exists(target_folder):
            print(Fore.RED + error_message["folder_not_found"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        
        break
    
    ques_sort_file = f"Sort file? {art('gimme')}"
    sort_file = questionary.select(ques_sort_file, radio_menu).ask()
    sort_file = radio_menu.index(sort_file) == 1
    
    while True:
        ques_start_index = f"Start index: {art('gimme')}"
        start_index = questionary.text(ques_start_index).ask()
        
        if start_index == "":
            start_index = 0
            break
        
        if not start_index.isdigit():
            print(Fore.RED + error_message["number_invalid"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        
        start_index = int(start_index)
        break
    
    main_process(target_folder, sort_file, start_index)

