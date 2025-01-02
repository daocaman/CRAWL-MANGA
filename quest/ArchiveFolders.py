from tasks.ArchiveFolders import main_process
from common.QuestCommon import yes_no_question, select_folder_question

def quest_form_archive_folders():
    
    is_multiple_folders = yes_no_question("Archive multiple folders?")
    target_folder = select_folder_question("Enter target folder: ")
    delete_folders = yes_no_question("Delete folders after archiving?")
    
    main_process(target_folder, is_multiple_folders, delete_folders)
