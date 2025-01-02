from tasks.MoveChapVol import main_process
from common.QuestCommon import select_file_question, text_question, yes_no_question

def quest_form_move_chap_vol():
    
    chap_vol_file = select_file_question("Enter chapters per volume file: ")
    
    manga_title = text_question("Enter manga title: ")

    delete_chap = yes_no_question("Delete folder chapters after copying? ")
    
    main_process(chap_vol_file, manga_title, delete_chap)
