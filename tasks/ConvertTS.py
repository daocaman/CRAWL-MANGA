import argparse
import sys
import os
from colorama import Fore, Style

from controllers.ConvertTS import convert_ts_to_mp4
from common.Constants import CONVERT_TS_DEBUG

def main_process(folder_path):
    if CONVERT_TS_DEBUG:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Tasks: ConvertTS'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"Folder path:":<20}' + Style.RESET_ALL + f'{folder_path: >49}')
    
    try:
        if not os.path.exists(folder_path):
            raise Exception(f'Folder {folder_path} does not exist')
        convert_ts_to_mp4(folder_path)
    except Exception as e:
        if CONVERT_TS_DEBUG:
            print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{str(e): >49}')
            print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(
        description='Convert ts files to mp4 files')
    parser.add_argument('-o', type=str, required=True, help='Target folder')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    main_process(args.o)

if __name__ == "__main__":
    main()
