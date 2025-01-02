from common.QuestCommon import select_folder_question
from tasks.ConvertTS import main_process

def quest_form_convert_ts():
    
    target_folder = select_folder_question("Enter target folder: ")
    
    main_process(target_folder)
    