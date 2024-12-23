import argparse
import sys
from colorama import Fore, Style

from controllers.ListAndRenameController import get_list_of_files
from common.Constants import LIST_AND_RENAME_DEBUG

def main_process(path: str):
    if LIST_AND_RENAME_DEBUG:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Tasks: CreateListFile'.center(70) + Style.RESET_ALL)
    try:
        get_list_of_files(path)
        if LIST_AND_RENAME_DEBUG:
            print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
    except Exception as e:
        if LIST_AND_RENAME_DEBUG:
            print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{e: >49}')
            print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)


def main():
    parser = argparse.ArgumentParser(
        description='Create file rename.json')
    parser.add_argument('-o', type=str, required=True, help='Target folder')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    main_process(args.o)

if __name__ == "__main__":
    main()
