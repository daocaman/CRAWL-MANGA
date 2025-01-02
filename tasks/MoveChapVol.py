import argparse
import sys
import os
import json
from colorama import Fore, Style
from pprint import pprint

from controllers.MoveChapController import move_chap_vol, MOVE_CHAP_VOL_DEBUG
from common.Constants import manga_vol
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_NO_MANGA_TITLE
from common.Validations import check_file_exists

def main_process(file_chapters: str, manga_title: str, delete_chapters: bool):
    """
    Main process for moving chapters into volumes
    :param file_chapters: str, file chapters
    :param manga_title: str, manga title
    :param delete_chapters: bool, delete chapters
    """
    if MOVE_CHAP_VOL_DEBUG:
        log_start_function("Tasks: MoveChapVol", "main_process")
        log_parameter("file_chapters", file_chapters, 1)
        log_parameter("manga_title", manga_title, 1)
        log_parameter("delete_chapters", delete_chapters, 1)
    
    try:
        check_file_exists(file_chapters)
                
        if not manga_title: 
            raise Exception(MSG_ERR_NO_MANGA_TITLE)
        
        with open(file_chapters, 'r') as f:
            chapters_per_volume = json.load(f)
            
        # pprint(chapters_per_volume)
        MOVE_CHAP_VOL_DEBUG and log_parameter("chapters_per_volume", chapters_per_volume, 2)
            
        for vol in chapters_per_volume:
            target_folder = manga_vol.format(manga_title, vol['vol'])
            move_chap_vol(target_folder, vol['start_chap'], vol['end_chap'], delete_chapters)
            
    except Exception as e:
        log_error("Tasks: MoveChapVol", "main_process", e)
        MOVE_CHAP_VOL_DEBUG and print(END_LOG)


def main():
    parser = argparse.ArgumentParser(
        description='Move chapters into volumes')
    parser.add_argument('-f', type=str, required=True, help='Chapters per volume in json format')
    parser.add_argument('-t', type=str, required=True, help='Manga title')
    parser.add_argument('-d', default=False, action='store_true', help='Delete folder chapters after copying')
    
    # Show help if no arguments provided    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    main_process(args.f, args.t, args.d)

    
if __name__ == '__main__':
    main()
