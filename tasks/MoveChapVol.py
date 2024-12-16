import argparse
import sys
import os
import json
from colorama import Fore, Style
from pprint import pprint
from common.Constants import MOVE_CHAP_VOL_DEBUG, manga_vol
from controllers.MoveChapController import move_chap_vol

def main():
    parser = argparse.ArgumentParser(
        description='Move chapters into volumes')
    parser.add_argument('-f', type=str, required=True, help='Chapters per volume in json format')
    parser.add_argument('-t', type=str, required=True, help='Manga title')
    parser.add_argument('-d', default=False, action='store_true', help='Delete folder chapters after copying')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    if MOVE_CHAP_VOL_DEBUG:
        print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'MoveChapVol: main'.center(70) + Style.RESET_ALL)
    
    try:
        if not os.path.exists(args.f):
            raise Exception('File not found')
        
        if not args.t: 
            raise Exception('Manga title not found')
        
        with open(args.f, 'r') as f:
            chapters_per_volume = json.load(f)
            
        pprint(chapters_per_volume)
            
        for vol in chapters_per_volume:
            target_folder = manga_vol.format(args.t, vol['vol'])
            print(target_folder)
            move_chap_vol(target_folder, vol['start_chap'], vol['end_chap'], args.d)
        
            
    except Exception as e:
        if MOVE_CHAP_VOL_DEBUG:
            print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
        return

    
if __name__ == '__main__':
    main()
