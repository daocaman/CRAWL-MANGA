from common.QuestCommon import select_folder_question
from tasks.ConvertTS import main_process
from common.Constants import folder_ts

def quest_form_convert_ts():
    
    target_folder = select_folder_question("Enter target folder (optional): ", folder_ts)
    
    main_process(target_folder)
    