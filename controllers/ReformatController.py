import os
import shutil
import json

from common.Constants import REFORMAT_DEBUG, file_prefix, file_chapters
from common.Commons import generate_filename, extract_number, is_image_file

def reformat_folder(folder='', is_delete=False):
    """
    Reformat a folder
    :param folder: Folder to reformat
    :param is_delete: Delete chapter folders
    :return: None
    """

    # Debug print initial
    REFORMAT_DEBUG and print("="*50)
    REFORMAT_DEBUG and print('Common: reformat_folder')
    REFORMAT_DEBUG and print(f"Folder: {folder}\nIs delete: {is_delete}")

    count = 0 # Image count
    
    # List folder and sort by chapter number
    folders = os.listdir(folder)
    folders = [f for f in folders if os.path.isdir(os.path.join(folder,f))]
    folders = sorted(folders, key=lambda x: extract_number(x, True, is_float=True))
    
    # Debug print folders
    REFORMAT_DEBUG and print(f"Folders: \n{'\n'.join(folders)}")
    
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
            new_name = generate_filename(file_prefix, count, ".jpg")
            shutil.copy(os.path.join(folder, fol, img),
                        os.path.join(folder, new_name))
            count += 1
        
        # Delete the chapter folder if is_delete is True
        if is_delete:
            shutil.rmtree(os.path.join(folder, fol))
    
    # Debug print list_chapters
    REFORMAT_DEBUG and print(f"List chapters: \n{'\n'.join([f'{chap['title']}: {chap['page']}' for chap in list_chapters])}")

    # Write the list of chapters to the file
    with open(os.path.join(folder, file_chapters), 'w+', encoding="utf-8") as json_file:
        # Write the list to the file
        json.dump(list_chapters, json_file, ensure_ascii=False, indent=4)
    
    # Debug print final
    REFORMAT_DEBUG and print("="*50)

