import argparse
import os
from colorama import Fore, Style
import sys
import concurrent.futures
from controllers.ResizeController import resize_image_process, RESIZE_DEBUG
from common.Commons import extract_number

def main_process(target_folder, is_multiple, is_horizontal):
    if RESIZE_DEBUG:
        print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Task: ResizeImages'.center(70) + Style.RESET_ALL)
    
    try:
        if is_multiple:
            folders = os.listdir()
            folders = [f for f in folders if os.path.isdir(f) and target_folder in f]
            folders = sorted(folders, key=lambda x: extract_number(x, True, True))
        
        resize_obj_list = []
        for fol in folders:
            resize_obj_list.append({
                "folder": fol,
                "is_horizontal": is_horizontal
            })
        
        if os.cpu_count() > 1:
            current_cpu = os.cpu_count() // 2
            RESIZE_DEBUG and print(Fore.CYAN + f'{"Multithreading supported:":<20}' + Style.RESET_ALL + f'{current_cpu}')
            with concurrent.futures.ThreadPoolExecutor(max_workers=current_cpu) as executor:
                executor.map(resize_image_process, resize_obj_list)
        else:
            for resize_obj in resize_obj_list:
                resize_image_process(resize_obj)

        RESIZE_DEBUG and print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)
    except Exception as e:
        if RESIZE_DEBUG:
            print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
            print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(
        description='Resize images')
    parser.add_argument('-o', type=str, required=True, help='Target folder')
    parser.add_argument('-m', action='store_true', help='Multiple folders')
    parser.add_argument('-hr', default=False, action='store_true', help='Resize to horizontal')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    main_process(args.o, args.m, args.hr)

if __name__ == "__main__":
    main()
