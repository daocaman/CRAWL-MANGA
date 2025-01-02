import argparse
import sys

from controllers.ResizeController import resize_image_process, RESIZE_DEBUG
from common.Commons import extract_number, execute_process
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Validations import check_and_get_list_of_folders

def main_process(target_folder: str, is_multiple: bool, is_horizontal: bool):
    """
    Main process for resizing images
    :param target_folder: str, target folder
    :param is_multiple: bool, is multiple folders
    :param is_horizontal: bool, is horizontal
    :return: None
    """
    
    if RESIZE_DEBUG:
        log_start_function("Tasks: ResizeImages", "main_process")
        log_parameter("target_folder", target_folder, 1)
        log_parameter("is_multiple", is_multiple, 1)
        log_parameter("is_horizontal", is_horizontal, 1)
    
    try:
        if is_multiple:
            folders = check_and_get_list_of_folders(target_folder)
            folders = sorted(folders, key=lambda x: extract_number(x, True, True))
        
        resize_obj_list = []
        for fol in folders:
            resize_obj_list.append({
                "folder": fol,
                "is_horizontal": is_horizontal
            })
        
        execute_process(resize_image_process, resize_obj_list)
        
        RESIZE_DEBUG and print(END_LOG)
    except Exception as e:
        log_error("Tasks: ResizeImages", "main_process", e)
        RESIZE_DEBUG and print(END_LOG)

def main():
    parser = argparse.ArgumentParser(
        description='Resize images')
    parser.add_argument('-o', type=str, required=True, help='Target folder')
    parser.add_argument('-m', action='store_true', help='Multiple folders')
    parser.add_argument('-hr', default=False, action='store_true', help='Resize to horizontal')

    # Show help if no arguments provided    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    main_process(args.o, args.m, args.hr)

if __name__ == "__main__":
    main()
