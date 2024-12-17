from art import art
import questionary
from colorama import Fore, Style
import os

from common.Constant_v1_1 import radio_menu, error_message
from tasks.ArchiveFolders import main_process

def quest_form_archive_folders():
    ques_is_multiple_folders = f"Archive multiple folders? {art('gimme')}"
    is_multiple_folders = questionary.select(ques_is_multiple_folders, radio_menu).ask()
    is_multiple_folders = radio_menu.index(is_multiple_folders)
    
    while True: 
        ques_target_folder = f"Enter target folder: {art('gimme')}"
        target_folder = questionary.text(ques_target_folder).ask()
        
        if target_folder == "":
            print(Fore.RED + error_message["folder"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        
        folders = os.listdir()  
        folders = [f for f in folders if os.path.isdir(f) and target_folder in f]
        if len(folders) == 0:
            print(Fore.RED + error_message["folder_not_found"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        break
    
    ques_delete_folders = f"Delete folders after archiving? {art('gimme')}"
    delete_folders = questionary.select(ques_delete_folders, radio_menu).ask()
    delete_folders = radio_menu.index(delete_folders) == 1
    
    main_process(target_folder, is_multiple_folders, delete_folders)
