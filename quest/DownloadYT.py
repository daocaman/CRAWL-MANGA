from art import art
import questionary
from colorama import Fore, Style
import os

from common.Constant_v1_1 import radio_menu, download_yt_menu, error_message, youtube_file_type
from tasks.DownloadYT import main_process

def quest_form_download_yt():
    
    ques_is_file_download = f"Type download: {art('gimme')}"
    is_file_download = questionary.select(ques_is_file_download, download_yt_menu).ask()
    is_file_download = download_yt_menu.index(is_file_download) == 1
    
    youtube_link = ""
    file_yt = "",
    type_download = "audio",
    link_type = 1,
    is_convert_mp4 = False
    
    if not is_file_download:
        ques_link_type = f"Is link playlist? {art('gimme')}"
        is_link_playlist = questionary.select(ques_link_type, radio_menu).ask()
        link_type = radio_menu.index(is_link_playlist) + 1
       
        while True:
            ques_link_yt = f"Enter link youtube: {art('gimme')}"
            youtube_link = questionary.text(ques_link_yt).ask()
            if youtube_link == "":
                print(Fore.RED + error_message["url"] + art("error", 3, 1) + Style.RESET_ALL)
                continue
        
            if link_type == 1 and not youtube_link.startswith("https://www.youtube.com/watch?v="):
                print(Fore.RED + error_message["url"] + art("error", 3, 1) + Style.RESET_ALL)
                print(Fore.CYAN + "Video link must start with https://www.youtube.com/watch?v=" + art("cat4") + Style.RESET_ALL)
                return
            
            if link_type == 2 and not youtube_link.startswith("https://www.youtube.com/playlist?list="):
                print(Fore.RED + error_message["url"] + art("error", 3, 1) + Style.RESET_ALL)
                print(Fore.CYAN + "Playlist link must start with https://www.youtube.com/playlist?list=" + art("cat4") + Style.RESET_ALL)
                return
            
            break
        
        file_yt = ""
        ques_type_download = f"Type download: {art('gimme')}"
        type_download = questionary.select(ques_type_download, youtube_file_type).ask()
        
    else:
        while True:
            ques_file_yt = f"Enter file youtube: {art('gimme')}"
            file_yt = questionary.text(ques_file_yt).ask()
            if file_yt == "":
                print(Fore.RED + error_message["file"] + art("error", 3, 1) + Style.RESET_ALL)
                continue
        
            if not os.path.exists(file_yt):
                print(Fore.RED + error_message["file_not_found"] + art("error", 3, 1) + Style.RESET_ALL)
                continue
        
            break
    
    ques_convert_mp4 = f"Convert to mp4? {art('gimme')}"
    is_convert_mp4 = questionary.select(ques_convert_mp4, radio_menu).ask()
    is_convert_mp4 = radio_menu.index(is_convert_mp4) == 1
    
    print(youtube_link, type_download, link_type, file_yt, is_convert_mp4)
    
    main_process(youtube_link, type_download, link_type, file_yt, is_convert_mp4)
        