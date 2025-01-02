from tasks.RenameFiles import main_process
from common.QuestCommon import select_folder_question, yes_no_question, number_question

def quest_form_rename_files():
    
    target_folder = select_folder_question("Enter target folder: ")
    sort_file = yes_no_question("Sort file? ")
    start_index = number_question("Start index: ", 0)
    
    main_process(target_folder, sort_file, start_index)

