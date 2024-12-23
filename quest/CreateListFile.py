import os
import questionary
from colorama import Fore, Style
from art import art

from common.Constant_v1_1 import error_message
from tasks.CreateListFile import main_process

def quest_form_create_list_file():
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
    
    main_process(target_folder)
    
    
