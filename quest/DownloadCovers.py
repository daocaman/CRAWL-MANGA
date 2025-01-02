from common.QuestCommon import url_question, number_question
from tasks.DownloadCovers import main_process

def quest_form_download_cover():
    
    manga_link = url_question("Enter manga link: ")
    number_of_covers = number_question("Enter number of covers (optional): ", 1)

    main_process(manga_link, number_of_covers)
