import argparse
import sys

from controllers.ReformatController import reformat_folders_process, REFORMAT_DEBUG
from common.Commons import execute_process
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Validations import check_and_get_list_of_folders

def main_process(target_folder: str, is_multiple: bool, is_delete: bool):
    """
    Main process for reformatting folders
    :param target_folder: str, target folder
    :param is_multiple: bool, is multiple folders
    :param is_delete: bool, is delete child folders after reformat
    """
    if REFORMAT_DEBUG:
        log_start_function("Tasks: Reformat", "main_process")
        log_parameter("target_folder", target_folder, 1)
        log_parameter("is_multiple", is_multiple, 1)
        log_parameter("is_delete", is_delete, 1)

        
    try:
        if is_multiple:
            
            folders = check_and_get_list_of_folders(target_folder)

            reformat_folders = []
            for fol in folders:
                reformat_folders.append({
                    'folder': fol,
                    'is_delete': is_delete
                })
            
            execute_process(reformat_folders_process, reformat_folders)
            
        else:
            reformat_folders_process({'folder': target_folder, 'is_delete': is_delete})

        REFORMAT_DEBUG and print(END_LOG)
    except Exception as e:
        log_error("Tasks: Reformat", "main_process", e)
        REFORMAT_DEBUG and print(END_LOG)


def main():
    parser = argparse.ArgumentParser(
        description='Reformat old folder')
    parser.add_argument('-o', type=str, required=True, help='Target folder')
    parser.add_argument('-m', default=False, action='store_true', help='Is multiple folders')
    parser.add_argument('-d', default=False, action='store_true', help='Is delete child folders after reformat')

    # Show help if no arguments provided    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    main_process(args.o, args.m, args.d)
   

if __name__ == "__main__":
    main()