import questionary
from colorama import Fore, Style
from art import art

from common.Constant_v1_1 import error_message
from tasks.ConvertTS import main_process

def quest_form_convert_ts():
    while True:
        ques_target_folder = f"Enter target folder: {art('gimme')}"
        target_folder = questionary.text(ques_target_folder).ask()
        
        if target_folder == "":
            print(Fore.RED + error_message["folder"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        
        break
    
    main_process(target_folder)
    