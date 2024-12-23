import argparse
import sys
import os
from colorama import Fore, Style

from controllers.DownloadM3U8 import download_m3u8
from common.Constants import DOWNLOAD_M3U8_DEBUG

def main_process(file_path):
    if DOWNLOAD_M3U8_DEBUG:
        print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Tasks: DownloadM3U8'.center(70) + Style.RESET_ALL)
    
    try:
        if not os.path.exists(file_path):
            raise Exception(f'File {file_path} does not exist')
        download_m3u8(file_path)
    except Exception as e:
        if DOWNLOAD_M3U8_DEBUG:
            print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{str(e): >49}')
            print(Fore.GREEN + '<' +'='*68 + '<' + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(
        description='Download manga')
    parser.add_argument('-f', type=str, required=True, help='M3U8 file path')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    main_process(args.f)

if __name__ == "__main__":
    main()