from tasks.DownloadM3U8 import main_process
from common.QuestCommon import select_file_question
from common.Constants import file_m3u8_mp4_json

def quest_form_download_m3u8():
    
    file_path = select_file_question("Enter file path (optional): ", file_m3u8_mp4_json)
    
    main_process(file_path)