import json
import m3u8_To_MP4

from common.Constants import DOWNLOAD_M3U8_DEBUG, folder_save_m3u8
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_CONTROLLER_DOWNLOAD_M3U8
from common.Validations import check_file_exist, check_and_create_folder

def download_m3u8(file_path: str):
    """
    Download m3u8 video from file path
    file_path: path to the file containing the m3u8 video information
    """
    
    if DOWNLOAD_M3U8_DEBUG:
        log_start_function("DownloadM3U8Controller", "download_m3u8")
        log_parameter("file_path", file_path, 1)
        
    try:
        
        check_file_exist(file_path)
        
        with open(file_path, 'r') as file:
            list_m3u8 = json.load(file)
        
        check_and_create_folder(folder_save_m3u8, create=True)
        
        for m3u8 in list_m3u8:
            url = m3u8["url"]
            output_path = m3u8["output_path"]
            m3u8_To_MP4.multithread_file_download(url, f'{folder_save_m3u8}/{output_path}')
            
        DOWNLOAD_M3U8_DEBUG and print(END_LOG)

    except Exception as e:
        if DOWNLOAD_M3U8_DEBUG:
            log_error("DownloadM3U8Controller", "download_m3u8", e)
        raise Exception(MSG_ERR_CONTROLLER_DOWNLOAD_M3U8.format("download_m3u8"))
