from common.QuestCommon import yes_no_question, select_folder_question
from tasks.ResizeImages import main_process

def quest_form_resize_images():
    is_multiple_folders = yes_no_question("Resize multiple folders? ")
    
    target_folder = select_folder_question("Enter target folder: ")
    
    is_horizontal = yes_no_question("Resize to horizontal? ")
        
    main_process(target_folder, is_multiple_folders, is_horizontal)
