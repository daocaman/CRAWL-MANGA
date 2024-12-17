import questionary
from colorama import Fore, Style
from art import art
import os

from common.Constant_v1_1 import radio_menu, error_message
from tasks.MoveChapVol import main_process

def quest_form_move_chap_vol():
    
    while True:
        ques_chap_vol_file = f"Enter chapters per volume file: {art('gimme')}"
        chap_vol_file = questionary.text(ques_chap_vol_file).ask()
        
        if chap_vol_file == "":
            print(Fore.RED + error_message["file"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        
        if not os.path.exists(chap_vol_file):
            print(Fore.RED + error_message["file_not_found"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        
        break
        
    while True:
        ques_manga_title = f"Enter manga title: {art('gimme')}"
        manga_title = questionary.text(ques_manga_title).ask()
        
        if manga_title == "":
            print(Fore.RED + error_message["manga_title"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        
        break
    
    ques_delete_chap = f"Delete folder chapters after copying? {art('gimme')}"
    delete_chap = questionary.select(ques_delete_chap, radio_menu).ask()
    delete_chap = radio_menu.index(delete_chap) == 1
    
    main_process(chap_vol_file, manga_title, delete_chap)
