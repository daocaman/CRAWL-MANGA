import argparse
import os
import sys
from colorama import Fore, Style
import concurrent.futures

from controllers.ReformatController import reformat_folder_process, reformat_folder, REFORMAT_DEBUG
from common.Commons import extract_number


def main():
    parser = argparse.ArgumentParser(
        description='Reformat old folder')
    parser.add_argument('-o', type=str, required=True, help='Target folder')
    parser.add_argument('-m', default=False, action='store_true', help='Is multiple folders')
    parser.add_argument('-d', default=False, action='store_true', help='Is delete child folders after reformat')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if REFORMAT_DEBUG:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Tasks: Reformat'.center(70) + Style.RESET_ALL)

    try:
        if args.m:
            folders = os.listdir()
            folders = [f for f in folders if os.path.isdir(f) and args.o in f]
            folders = sorted(folders, key=lambda x: extract_number(x, True))

            if len(folders) == 0:
                raise Exception('No folders found')

            reformat_folders = []
            for fol in folders:
                reformat_folders.append({
                    'folder': fol,
                    'is_delete': args.d
                })

            if os.cpu_count() > 1:
                current_cpu = os.cpu_count() // 2
                REFORMAT_DEBUG and print(Fore.CYAN + f'{"Multithreading supported:":<20}' + Style.RESET_ALL + f'{current_cpu}')
                with concurrent.futures.ThreadPoolExecutor(max_workers=current_cpu) as executor:
                    executor.map(reformat_folder_process, reformat_folders)
            else:
                for reformat_obj in reformat_folders:
                    reformat_folder_process(reformat_obj)


        else:
            reformat_folder(args.o, args.d)

        REFORMAT_DEBUG and print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
    except Exception as e:
        if REFORMAT_DEBUG:
            print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
            print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)


if __name__ == "__main__":
    main()