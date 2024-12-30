import os
import shutil

from common.Constants import ARCHIVE_DEBUG, file_chapters
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_CONTROLLER_ARCHIVE
from common.Validations import check_and_create_folder

def archive_folder(folder: str='', is_delete: bool=False):
    """
    Archive a folder
    :param folder: folder to archive
    :param is_delete: delete the folder after archiving
    :return: None
    """
    
    # Debug print initial
    if ARCHIVE_DEBUG:
        log_start_function("ArchiveController", "archive_folder")
        log_parameter("Folder", folder, 1)
        log_parameter("Is delete", is_delete, 1)
        print(END_LOG)
        
    try:
    
        check_and_create_folder(folder, True)
    
        # Check if the folder exists
        if os.path.exists(f'{folder}/{file_chapters}'):
            os.remove(f'{folder}/{file_chapters}')

        # Archive the folder    
        shutil.make_archive(folder, "zip", base_dir=folder)
        
        # Delete the folder if is_delete is True
        if is_delete:
            shutil.rmtree(folder)

        # Debug print final
        ARCHIVE_DEBUG and print(END_LOG)
    except Exception as e:
        if ARCHIVE_DEBUG:
            log_error("ArchiveController", "archive_folder", e)
        raise Exception(MSG_ERR_CONTROLLER_ARCHIVE.format("archive_folder"))

def archive_folder_process(process_obj):
    """
    Process the archive folder
    :param process_obj: process object
    :return: None
    """
    archive_folder(process_obj["folder"], process_obj["is_delete"])
