from common.QuestCommon import yes_no_question, select_folder_question, select_file_question
from tasks.CreateMetadata import main_process
from common.Constants import file_comic_json, file_bookmarks

def quest_form_create_metadata():
    
    is_multiple_folders = yes_no_question("Is multiple folders?")
    target_folder = select_folder_question("Enter target folder: ")
    comic_info = select_file_question("Enter comic info file: ", file_comic_json)
    bookmark = select_file_question("Enter bookmark file: ", file_bookmarks)

    main_process(bookmark, comic_info, target_folder, is_multiple_folders)

