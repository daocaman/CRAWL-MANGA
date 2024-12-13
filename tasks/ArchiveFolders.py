import argparse
import os
import sys
from colorama import Fore, Style
import multiprocessing

from common.Commons import extract_number
from controllers.ArchiveController import archive_folder_process, ARCHIVE_DEBUG
from controllers.ResizeController import resize_image_process

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

    ARCHIVE_DEBUG and print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)
    ARCHIVE_DEBUG and print(Fore.YELLOW + 'Tasks: ArchiveFolders'.center(70) + Style.RESET_ALL)

    try:
        if args.m:
            folders = os.listdir()
            folders = [f for f in folders if os.path.isdir(f) and args.o in f]
            folders = sorted(folders, key=lambda x: extract_number(x, True))
            if len(folders) == 0:
                raise Exception('No folders found')

            resize_obj_list = []
            for fol in folders:
                resize_obj_list.append({
                    "folder": fol,
                    "is_horizontal": False
                })

            if os.cpu_count() > 1:
                with multiprocessing.Pool(os.cpu_count() // 2) as pool:  
                    pool.map(resize_image_process, resize_obj_list)
            else:
                for resize_obj in resize_obj_list:
                    resize_image_process(resize_obj)

            folders_process = []
            for fol in folders:
                folders_process.append({
                    "folder": fol,
                    "is_delete": args.d
                })

            if os.cpu_count() > 1:
                ARCHIVE_DEBUG and print(Fore.CYAN + f'{"Multithreading supported:":<20}' + Style.RESET_ALL + f'{os.cpu_count()}')
                with multiprocessing.Pool(os.cpu_count() // 2) as pool:  
                    pool.map(archive_folder_process, folders_process)
        else:
            if not os.path.isdir(args.o):
                raise Exception('Target folder not found')

            archive_folder_process({
                "folder": args.o,
                "is_delete": args.d
            })

    except Exception as e:
        ARCHIVE_DEBUG and print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{str(e): >49}')
        ARCHIVE_DEBUG and print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)

if __name__ == "__main__":
    main()
