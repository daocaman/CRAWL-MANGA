import os
import ffmpeg

from common.Constants import CONVERT_TS_DEBUG, folder_ts
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_CONTROLLER_CONVERT_TS
from common.Validations import check_and_create_folder

def convert_ts_to_mp4(folder_path: str = ''):
    """
    Convert all ts files in a folder to mp4 files
    :param folder_path: The path to the folder containing the ts files
    :return: None
    """
    if CONVERT_TS_DEBUG:
        log_start_function("ConvertTSController", "convert_ts_to_mp4")
        log_parameter("Folder path", folder_path, 1)
    
    try:
        folder_path = folder_path if folder_path else folder_ts
        
        check_and_create_folder(folder_path, True)
            
        files = os.listdir(folder_path)
        files = [file for file in files if file.endswith('.ts')]
        
        if CONVERT_TS_DEBUG:
            log_parameter("Files", files, 2)
        
        for file in files:
            input_file = ffmpeg.input(os.path.join(folder_path, file))
            output_file = os.path.join(folder_path, file.replace('.ts', '.mp4'))
            ffmpeg.output(input_file, output_file, vcodec='libx264').global_args('-threads', str(os.cpu_count()//2)).run()
            
        if CONVERT_TS_DEBUG:
            print(END_LOG)
        
    except Exception as e:
        if CONVERT_TS_DEBUG:
            log_error("ConvertTSController", "convert_ts_to_mp4", e)
        raise Exception(MSG_ERR_CONTROLLER_CONVERT_TS.format("convert_ts_to_mp4"))
        