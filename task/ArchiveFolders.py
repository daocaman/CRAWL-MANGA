import argparse
import os
import sys
from colorama import Fore, Style

from common.Commons import extract_number
from controllers.ArchiveController import archive_folder, ARCHIVE_DEBUG


def main():
    parser = argparse.ArgumentParser(
        description='Archive folders')
    parser.add_argument('-o', type=str, required=True, help='Target folder')
    parser.add_argument('-m', action='store_true', help='Is multiple folders')
    parser.add_argument('-d', default=False, action='store_true', help='Is delete folders after archiving')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    ARCHIVE_DEBUG and print(Fore.GREEN + '='*70 + Style.RESET_ALL)
    ARCHIVE_DEBUG and print(Fore.YELLOW + 'Tasks: ArchiveFolders'.center(70) + Style.RESET_ALL)

    try:
        if args.m:
            folders = os.listdir()
            folders = [f for f in folders if os.path.isdir(f) and args.o in f]
            folders = sorted(folders, key=lambda x: extract_number(x, True))
            for fol in folders:
                archive_folder(fol, args.d)
        else:
            archive_folder(args.o, args.d)
    except Exception as e:
        ARCHIVE_DEBUG and print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{str(e): >49}')
        ARCHIVE_DEBUG and print(Fore.GREEN + '='*70 + Style.RESET_ALL)

if __name__ == "__main__":
    main()
