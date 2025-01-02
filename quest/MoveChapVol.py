from tasks.MoveChapVol import main_process
from common.QuestCommon import select_file_question, text_question, yes_no_question
from common.Constants import file_vol_chaps

def quest_form_move_chap_vol():
    
    chap_vol_file = select_file_question("Enter chapters per volume file: ", file_vol_chaps)
    
    manga_title = text_question("Enter manga title: ")

    delete_chap = yes_no_question("Delete folder chapters after copying? ")
    
    main_process(chap_vol_file, manga_title, delete_chap)
