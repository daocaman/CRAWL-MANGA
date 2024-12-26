import argparse
import sys
from colorama import Fore, Style

from controllers.DownloadNovelController import DOWNLOAD_NOVEL_DEBUG, download_novel

def main_process(novel_id: str, server: int, start_index: int, end_index: int, title: str, author: str):
    try:
        if DOWNLOAD_NOVEL_DEBUG:
            print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
            print(Fore.YELLOW + 'DownloadNovel: main_process'.center(70) + Style.RESET_ALL)
            print(Fore.BLUE + f'{"Novel id:":<20}' + Style.RESET_ALL + f'{novel_id: >49}')
            print(Fore.BLUE + f'{"Server:":<20}' + Style.RESET_ALL + f'{server: >49}')
            print(Fore.BLUE + f'{"Start index:":<20}' + Style.RESET_ALL + f'{start_index: >49}')
            print(Fore.BLUE + f'{"End index:":<20}' + Style.RESET_ALL + f'{end_index: >49}')
        
        if novel_id == "":
            raise Exception("Novel id is required")
        
        download_novel(server, start_index, end_index, novel_id, title, author)
    except Exception as e:
        if DOWNLOAD_NOVEL_DEBUG:
            print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{e: >49}')
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
  

def main():
    parser = argparse.ArgumentParser(
        description='Download novel')
    parser.add_argument('-id', type=str, required=True, help='Id of the novel')
    parser.add_argument('-s', type=int, default=1, required=True, help='Server to download from')
    parser.add_argument('-s_i', type=int, default=1, required=False, help='Start index')
    parser.add_argument('-e_i', type=int, default=10, required=False, help='End index')
    parser.add_argument('-t', type=str, required=True, help='Title of the novel')
    parser.add_argument('-a', type=str, required=True, help='Author of the novel')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    main_process(args.id, args.s, args.s_i, args.e_i, args.t, args.a)

if __name__ == "__main__":
    main()  
