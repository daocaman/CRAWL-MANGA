from art import art
import questionary
from colorama import Fore, Style
import os

from common.Constants import folder_running_resource
from common.Constant_v1_1 import radio_menu, error_message
from common.Validations import check_and_get_list_of_folders, check_valid_video_url, check_valid_playlist_url

def wrong_input(message: str):
    """
    Print wrong input message
    :param message: message to print
    """
    message = Fore.RED + message + art("error", 3, 1) + Style.RESET_ALL
    print(message)


def yes_no_question(question: str):
    """
    Ask a yes or no question
    :param question: question to ask
    :return: True if yes, False if no
    """
    ques_sentence = f"{question} {art('gimme')}"
    answer = questionary.select(ques_sentence, radio_menu).ask()
    answer = radio_menu.index(answer)
    return answer == 1

def select_question(question: str, options: list):
    """
    Ask a select question
    :param question: question to ask
    :param options: options to select
    :return: index of the selected option
    """
    ques_sentence = f"{question} {art('gimme')}"
    answer = questionary.select(ques_sentence, options).ask()
    return options.index(answer)

def select_folder_question(question: str, default_folder: str=""):
    """
    Ask a select folder question
    :param question: question to ask
    :param default_folder: default folder
    :return: folder name
    """
    ques_sentence = f"{question} {art('gimme')}"
    answer = ""
    
    while True: 
        answer = questionary.text(ques_sentence).ask()
        
        if answer == "":
            if default_folder != "":
                answer = default_folder
                break
            else:
                wrong_input(error_message["folder"])
                continue
        
        folders = check_and_get_list_of_folders(answer, alert=False)
        if len(folders) == 0:
            wrong_input(error_message["folder_not_found"])
            continue
        break
    
    return answer

def select_file_question(question: str, default_file: str=""):
    """
    Ask a select file question
    :param question: question to ask
    :param default_file: default file
    :return: file name
    """
    ques_sentence = f"{question} {art('gimme')}"
    answer = ""
    
    while True:
        answer = questionary.text(ques_sentence).ask()
        if answer == "":
            if default_file != "":
                answer = f'{folder_running_resource}/{default_file}'
                break
            else:
                wrong_input(error_message["file"])
                continue
        
        if not os.path.exists(answer):
            wrong_input(error_message["file_not_found"])
            continue
        break
    
    return answer

def url_question(question: str):
    """
    Ask a url question
    :param question: question to ask
    :return: url
    """
    ques_sentence = f"{question} {art('gimme')}"
    answer = ""
    
    while True:
        answer = questionary.text(ques_sentence).ask()
        if answer == "" or "https://" not in answer:
            wrong_input(error_message["url"])
            continue
        break
    return answer

def number_question(question: str, default: int = 1):
    """
    Ask a number question
    :param question: question to ask
    :param default: default number
    :return: number
    """
    ques_sentence = f"{question} {art('gimme')}"
    answer = ""
    
    while True:
        answer = questionary.text(ques_sentence).ask()
        if answer == "":
            answer = default
            break
        
        if not answer.isdigit():
            wrong_input(error_message["number_invalid"])
            continue
        break
    return int(answer)

def text_question(question: str, default: str = ""):
    """
    Ask a text question
    :param question: question to ask
    :param default: default text
    :return: text
    """
    ques_sentence = f"{question} {art('gimme')}"
    answer = ""
    
    while True:
        answer = questionary.text(ques_sentence).ask()
        if answer == "":
            if default != "":
                answer = default
                break
            else:
                wrong_input(error_message["text"])
                continue
        break
    return answer

def ytb_link_question(question: str, is_link_playlist: bool):
    """
    Ask a youtube link question
    :param question: question to ask
    :param is_link_playlist: is link playlist
    :return: youtube link
    """
    ques_sentence = f"{question} {art('gimme')}"
    answer = ""
    
    while True:
        answer = questionary.text(ques_sentence).ask()
        if answer == "" or "https://" not in answer:
            wrong_input(error_message["url"])
            continue
        
        if not is_link_playlist and not check_valid_video_url(answer, False):
            wrong_input(error_message["url"])
            continue
            
        if is_link_playlist and not check_valid_playlist_url(answer, False):
            wrong_input(error_message["url"])
            continue
        break
    return answer

def quality_question(question: str, default: str = "720"):
    """
    Ask a quality question
    :param question: question to ask
    :param default: default quality
    :return: quality
    """
    ques_sentence = f"{question} {art('gimme')}"
    answer = ""
    
    while True:
        answer = questionary.text(ques_sentence).ask()
        if answer == "":
            answer = default
            break
        if answer not in ["144", "240", "360", "480", "720", "1080"]:
            wrong_input(error_message["quality"])
            continue
        break
    return answer

