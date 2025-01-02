import os
import shutil
import json

from common.Commons import generate_filename, extract_number, is_image_file
from common.Constants import REFORMAT_DEBUG, prefix_image_file, file_chapters
from common.Messages import log_start_function, log_parameter, END_LOG, log_error
from common.Messages import MSG_ERR_CONTROLLER_REFORMAT

def reformat_folder(folder: str='', is_delete: bool = False):
    """
    Reformat a folder
    :param folder: Folder to reformat
    :param is_delete: Delete chapter folders
    :return: None
    """

    # Debug print initial
    if REFORMAT_DEBUG:
        log_start_function("ReformatController", "reformat_folder")
        log_parameter("Folder", folder, 1)
        log_parameter("Is delete", is_delete, 1)

    try:
        count = 0 # Image count
        
        # List folder and sort by chapter number
        folders = os.listdir(folder)
        folders = [f for f in folders if os.path.isdir(os.path.join(folder,f))]
        folders = sorted(folders, key=lambda x: extract_number(x, True, is_float=True))
        
        # Debug print folders
        if REFORMAT_DEBUG:
            log_parameter("Folders", folders, 2)
        
        # List chapters
        list_chapters = []
        for fol in folders:
            list_chapters.append({
                "title": fol,
                "page": count
            })
            
            # List images in the chapter folder
            images = os.listdir(os.path.join(folder, fol))
            images = [f for f in images if is_image_file(f)]
            images = sorted(images, key=lambda x: extract_number(x, is_float=True))

            # Copy and rename images to the parent folder
            for img in images:
                new_name = generate_filename(prefix_image_file, count, ".jpg")
                shutil.copy(os.path.join(folder, fol, img),
                            os.path.join(folder, new_name))
                count += 1
            
            # Delete the chapter folder if is_delete is True
            if is_delete:
                shutil.rmtree(os.path.join(folder, fol))
        
        # Debug print list_chapters
        if REFORMAT_DEBUG:
            log_parameter("List chapters", list_chapters, 2)

        # Write the list of chapters to the file
        with open(os.path.join(folder, file_chapters), 'w+', encoding="utf-8") as json_file:
            # Write the list to the file
            json.dump(list_chapters, json_file, ensure_ascii=False, indent=4)
        
        # Debug print final
        REFORMAT_DEBUG and print(END_LOG)
        
    except Exception as e:
        if REFORMAT_DEBUG:
            log_error("ReformatController", "reformat_folder", e)
        raise Exception(MSG_ERR_CONTROLLER_REFORMAT.format(e))


def reformat_folders_process(reformat_obj):
    """
    Process reformat folders
    :param reformat_obj: Reformat object
    :return: None
    """
    reformat_folder(reformat_obj['folder'], reformat_obj['is_delete'])