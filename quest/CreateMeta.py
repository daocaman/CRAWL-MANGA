import questionary
from art import art
import os
from colorama import Fore, Style

from common.Constant_v1_1 import radio_menu, error_message
from tasks.CreateMetadata import main_process

def quest_form_create_metadata():
    ques_is_multiple_folders = f"Is multiple folders? {art('gimme')}"
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
    
    while True:
        ques_comic_info = f"Enter comic info file: {art('gimme')}"
        comic_info = questionary.text(ques_comic_info).ask()
        
        if comic_info == "":
            print(Fore.RED + error_message["file"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        
        if not os.path.exists(comic_info):
            print(Fore.RED + error_message["file_not_found"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        break
    
    while True:
        ques_bookmark = f"Enter bookmark file: {art('gimme')}"
        bookmark = questionary.text(ques_bookmark).ask()
        
        if bookmark == "":
            break
        
        if not os.path.exists(bookmark):
            print(Fore.RED + error_message["file_not_found"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        break
    
    main_process(bookmark, comic_info, target_folder, is_multiple_folders)

