import questionary
from art import art
from colorama import Fore, Style
from common.Constant_v1_1 import manga_menu, error_message
from tasks.DownloadManga import main_process

def quest_form_download_manga():
    # Link manga
    ques_link = f"Enter manga link: {art('gimme')}"
    
    while True:
        manga_link = questionary.text(ques_link).ask()
        
        if manga_link == "" or "https://" not in manga_link:
            print(Fore.RED + error_message["url"] + art("error", 3, 1) + Style.RESET_ALL)
            continue
        break
    
    # Select server
    ques_server = f"Select server: {art('gimme')}"
    server = questionary.select(ques_server, manga_menu).ask()
    server = manga_menu.index(server) + 1
    
    # Number of chapter
    ques_number_of_chapter = f"Enter number of chapter (optional): {art('gimme')}"
    while True:
        number_of_chapter = questionary.text(ques_number_of_chapter).ask()
        
        if number_of_chapter == "":
            number_of_chapter = -1
            break
        
        if not number_of_chapter.isdigit():
            print(Fore.RED + error_message["number_invalid"] + art("error", 3, 1) + Style.RESET_ALL)
            continue

        number_of_chapter = int(number_of_chapter)
        break
    
    # Start from index
    ques_start_from_index = f"Enter start from index (optional): {art('gimme')}"
    while True:
        start_from_index = questionary.text(ques_start_from_index).ask()
        if start_from_index == "":
            start_from_index = -1
            break
        
        if not start_from_index.isdigit():
            print(Fore.RED + error_message["number_invalid"] + art("error", 3, 1) + Style.RESET_ALL)
            continue

        start_from_index = int(start_from_index)
        break

    main_process(manga_link, number_of_chapter, server, start_from_index)
    
    
    