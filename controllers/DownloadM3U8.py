import json
import os
from colorama import Fore, Style
import m3u8_To_MP4

from common.Constants import DOWNLOAD_M3U8_DEBUG, save_m3u8_file

def download_m3u8(file_path):
    """
    Download m3u8 video from file path
    file_path: path to the file containing the m3u8 video information
    """
    
    if DOWNLOAD_M3U8_DEBUG:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'DownloadM3U8Controller: download_m3u8'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"File path:":<20}' + Style.RESET_ALL + f'{file_path: >49}')
    
    with open(file_path, 'r') as file:
        list_m3u8 = json.load(file)
        
    if not os.path.exists(save_m3u8_file):
        os.makedirs(save_m3u8_file)
    
    for m3u8 in list_m3u8:
        url = m3u8["url"]
        output_path = m3u8["output_path"]
        m3u8_To_MP4.multithread_file_download(url, f'{save_m3u8_file}/{output_path}')