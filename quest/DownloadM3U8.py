import questionary
import os
from art import art
from colorama import Fore, Style    

from common.Constant_v1_1 import error_message
from tasks.DownloadM3U8 import main_process

def quest_form_download_m3u8():
    while True:
        ques_file_path = f"Enter file path: {art('gimme')}"
        file_path = questionary.text(ques_file_path).ask()
        if not os.path.exists(file_path):
            print(Fore.RED + error_message["url"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        break
    main_process(file_path)