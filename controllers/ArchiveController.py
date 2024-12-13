import os
import shutil

from common.Constants import ARCHIVE_DEBUG, file_chapters

def archive_folder(folder='', is_delete=False):
    """
    Archive a folder
    :param folder: folder to archive
    :param is_delete: delete the folder after archiving
    :return: None
    """
    
    # Debug print initial
    ARCHIVE_DEBUG and print("="*50)
    ARCHIVE_DEBUG and print('Common: archive_folder')
    ARCHIVE_DEBUG and print(f"Folder: {folder}\nIs delete: {is_delete}")
    
    # Check if the folder exists
    if os.path.exists(f'{folder}/{file_chapters}'):
        os.remove(f'{folder}/{file_chapters}')

    # Archive the folder    
    shutil.make_archive(folder, "zip", base_dir=folder)
    
    # Delete the folder if is_delete is True
    if is_delete:
        shutil.rmtree(folder)

    # Debug print final
    ARCHIVE_DEBUG and print("="*50)


