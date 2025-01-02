from tasks.DownloadM3U8 import main_process
from common.QuestCommon import select_file_question

def quest_form_download_m3u8():
    
    file_path = select_file_question("Enter file path: ")
    
    main_process(file_path)