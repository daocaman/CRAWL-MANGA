import os
from colorama import Fore, Style
from pprint import pprint
import ffmpeg

from common.Constants import CONVERT_TS_DEBUG

def convert_ts_to_mp4(folder_path):
    """
    Convert all ts files in a folder to mp4 files
    :param folder_path: The path to the folder containing the ts files
    """
    if CONVERT_TS_DEBUG:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'ConvertTSController: convert_ts_to_mp4'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"Folder path:":<20}' + Style.RESET_ALL + f'{folder_path: >49}')
        
    files = os.listdir(folder_path)
    files = [file for file in files if file.endswith('.ts')]
    
    if CONVERT_TS_DEBUG:
        print(Fore.BLUE + f'{"Files:":<20}' + Style.RESET_ALL)
        pprint(files)
    
    for file in files:
        input_path = os.path.join(folder_path, file)
        output_path = os.path.join(folder_path, file.replace('.ts', '.mp4'))
        
        ffmpeg.input(input_path).output(output_path).run()
