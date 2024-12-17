import questionary
from colorama import Fore, Style
from art import art
import os

from common.Constant_v1_1 import radio_menu, error_message
from tasks.Reformat import main_process

def quest_form_reformat():
    ques_is_multiple = f"Is multiple folder? {art('gimme')}"
    is_multiple = questionary.select(ques_is_multiple, radio_menu).ask()
    is_multiple = radio_menu.index(is_multiple) == 1
    
    while True:
        ques_target_folder = f"Enter target folder: {art('gimme')}"
        target_folder = questionary.text(ques_target_folder).ask()
        
        if target_folder == "":
            print(Fore.RED + error_message["folder"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        
        if not os.path.exists(target_folder) and not is_multiple:
            print(Fore.RED + error_message["folder_not_found"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
            
        if is_multiple:
            folders = os.listdir()
            folders = [f for f in folders if os.path.isdir(f) and target_folder in f]
            if len(folders) == 0:
                print(Fore.RED + error_message["folder_not_found"] + art("error", 3, 1) + Style.RESET_ALL)
                continue

        break
    
    ques_delete_child_folder = f"Delete child folder after reformat? {art('gimme')}"
    delete_child_folder = questionary.select(ques_delete_child_folder, radio_menu).ask()
    delete_child_folder = radio_menu.index(delete_child_folder) == 1
    
    main_process(target_folder, is_multiple, delete_child_folder)
