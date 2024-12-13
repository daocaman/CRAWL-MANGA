import argparse
import os
from colorama import Fore, Style
import sys

from controllers.ResizeController import resize_image, RESIZE_DEBUG
from common.Commons import extract_number

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
    
    RESIZE_DEBUG and print(Fore.GREEN + '='*70 + Style.RESET_ALL)
    RESIZE_DEBUG and print(Fore.YELLOW + 'Task: ResizeImages'.center(70) + Style.RESET_ALL)
    
    try:
        if args.m:
            folders = os.listdir()
            folders = [f for f in folders if os.path.isdir(f) and args.o in f]
        folders = sorted(folders, key=lambda x: extract_number(x, True, True))
        for fol in folders:
            resize_image(fol, args.hr)
    except Exception as e:
        RESIZE_DEBUG and print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
        RESIZE_DEBUG and print(Fore.GREEN + '='*70 + Style.RESET_ALL)

if __name__ == "__main__":
    main()
