import argparse
import sys

from controllers.ArchiveController import archive_folder_process, ARCHIVE_DEBUG
from controllers.ResizeController import resize_image_process
from common.Commons import execute_process
from common.Messages import log_start_function, END_LOG, log_parameter, log_error
from common.Validations import check_and_get_list_of_folders, check_and_create_folder

def main_process(target_folder: str, is_multiple_folders: bool, is_delete_folders: bool):
    """
    Main process
    :param target_folder: The target folder
    :param is_multiple_folders: Is multiple folders
    :param is_delete_folders: Is delete folders
    :return: None
    """
    if ARCHIVE_DEBUG:
        log_start_function("Tasks: ArchiveFolders", "main_process")
        log_parameter("Target folder", target_folder, 1)
        log_parameter("Is multiple folders", is_multiple_folders, 1)
        log_parameter("Is delete folders", is_delete_folders, 1)

    try:
        if is_multiple_folders:
            
            folders = check_and_get_list_of_folders(target_folder)

            # List resize object for processing resize images
            resize_obj_list = []
            for fol in folders:
                resize_obj_list.append({
                    "folder": fol,
                    "is_horizontal": False
                })

            # Resize images before archiving
            execute_process(resize_image_process, resize_obj_list)
          
            # List archive object for processing archive folders
            folders_process = []
            for fol in folders:
                folders_process.append({
                    "folder": fol,
                    "is_delete": is_delete_folders
                })  

            # Archive folders
            execute_process(archive_folder_process, folders_process)
            
        else:
            check_and_create_folder(target_folder, alert=True)

            archive_folder_process({
                "folder": target_folder,
                "is_delete": is_delete_folders
            })
        
        ARCHIVE_DEBUG and print(END_LOG)

    except Exception as e:
        log_error("Tasks: ArchiveFolders", "main_process", e)
        ARCHIVE_DEBUG and print(END_LOG)

def main():
    parser = argparse.ArgumentParser(
        description='Archive folders')
    parser.add_argument('-o', type=str, required=True, help='Target folder')
    parser.add_argument('-m', action='store_true', help='Is multiple folders')
    parser.add_argument('-d', default=False, action='store_true', help='Is delete folders after archiving')

    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    main_process(args.o, args.m, args.d)


if __name__ == "__main__":
    main()
