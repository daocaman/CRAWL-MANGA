from common.Constant_v1_1 import manga_menu
from tasks.DownloadManga import main_process
from common.QuestCommon import url_question, select_question, number_question

def quest_form_download_manga():
    
    manga_link = url_question("Enter manga link: ")
    server = select_question("Select server: ", manga_menu)
    server = server + 1
    number_of_chapter = number_question("Enter number of chapter (optional): ", -1)
    start_from_index = number_question("Enter start from index (optional): ", -1)

    main_process(manga_link, number_of_chapter, server, start_from_index)
    
    
    