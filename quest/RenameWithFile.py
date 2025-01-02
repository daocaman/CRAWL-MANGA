from tasks.RenameWithFile import main_process
from common.QuestCommon import yes_no_question

def quest_form_rename_with_file():
    
    is_confirm = yes_no_question("Are you sure to rename? ")
    if not is_confirm:
        return
    
    main_process()
       
