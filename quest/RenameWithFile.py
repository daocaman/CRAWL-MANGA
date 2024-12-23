import questionary
from art import art

from common.Constant_v1_1 import radio_menu
from tasks.RenameWithFile import main_process

def quest_form_rename_with_file():
    ques_confirm = f"Are you sure to rename? {art('gimme')}"
    is_confirm = questionary.select(ques_confirm, radio_menu).ask()
    if is_confirm == "No":
        return
    
    main_process()
       
