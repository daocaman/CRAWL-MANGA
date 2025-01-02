from art import art
import questionary
from colorama import Fore, Style
import os

from common.Constant_v1_1 import radio_menu, download_yt_menu, error_message, youtube_file_type
from tasks.DownloadYT import main_process
from common.QuestCommon import select_question, yes_no_question, ytb_link_question, quality_question, select_file_question

def quest_form_download_yt():
    
    is_file_download = select_question("Type download: ", download_yt_menu)
    is_file_download = download_yt_menu.index(is_file_download) == 1
    
    youtube_link = ""
    file_yt = "",
    type_download = "audio",
    link_type = 1,
    quality = "720"
    
    if not is_file_download:
        is_link_playlist = yes_no_question("Is link playlist? ")
        link_type = radio_menu.index(is_link_playlist) + 1
       
        youtube_link = ytb_link_question("Enter link youtube: ", is_link_playlist)
        quality = quality_question("Quality: ", "720")
        
        file_yt = ""
        type_download = select_question("Type download: ", youtube_file_type)
        
    else:
        file_yt = select_file_question("Enter file youtube: ")
      
    main_process(youtube_link, type_download, link_type, file_yt, quality)
        