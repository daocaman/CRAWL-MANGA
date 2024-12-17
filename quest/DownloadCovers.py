from art import art
import questionary
from colorama import Fore, Style

from common.Constant_v1_1 import error_message
from tasks.DownloadCovers import main_process

def quest_form_download_cover():
    
    while True:
        ques_link = f"Enter manga link: {art('gimme')}"
        manga_link = questionary.text(ques_link).ask()
        
        if manga_link == "" or "https://" not in manga_link:
            print(Fore.RED + error_message["url"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        break
    
    while True:
        ques_number_of_covers = f"Enter number of covers (optional): {art('gimme')}"
        number_of_covers = questionary.text(ques_number_of_covers).ask()
        
        if number_of_covers == "":
            number_of_covers = 1
            break
        
        if not number_of_covers.isdigit():
            print(Fore.RED + error_message["number_invalid"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        break
    
    main_process(manga_link, number_of_covers)
