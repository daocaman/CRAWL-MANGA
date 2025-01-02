from common.QuestCommon import select_folder_question
from tasks.CreateListFile import main_process

def quest_form_create_list_file():     
     
    target_folder = select_folder_question("Enter target folder: ")
    
    main_process(target_folder)
    