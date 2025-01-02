import questionary
from colorama import Fore, Style
from art import art
import os

from common.Constant_v1_1 import radio_menu, error_message
from common.QuestCommon import yes_no_question, select_folder_question
from tasks.Reformat import main_process

def quest_form_reformat():
    
    is_multiple = yes_no_question("Is multiple folder? ")
    target_folder = select_folder_question("Enter target folder: ")
    delete_child_folder = yes_no_question("Delete child folder after reformat? ")
    
    main_process(target_folder, is_multiple, delete_child_folder)
