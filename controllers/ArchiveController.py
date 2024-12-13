import os
import shutil
from colorama import Fore, Style

from common.Constants import ARCHIVE_DEBUG, file_chapters

def archive_folder(folder='', is_delete=False):
    """
    Archive a folder
    :param folder: folder to archive
    :param is_delete: delete the folder after archiving
    :return: None
    """
    
    # Debug print initial
    ARCHIVE_DEBUG and print(Fore.GREEN + '='*70 + Style.RESET_ALL)
    ARCHIVE_DEBUG and print(Fore.YELLOW + 'ArchiveController: archive_folder'.center(70) + Style.RESET_ALL)
    ARCHIVE_DEBUG and print(Fore.BLUE + f'{"Folder:":<20}' + Style.RESET_ALL + f'{folder: >49}')
    ARCHIVE_DEBUG and print(Fore.BLUE + f'{"Is delete:":<20}' + Style.RESET_ALL + f'{str(is_delete): >49}')
   
    # Check if the folder exists
    if os.path.exists(f'{folder}/{file_chapters}'):
        os.remove(f'{folder}/{file_chapters}')

    # Archive the folder    
    shutil.make_archive(folder, "zip", base_dir=folder)
    
    # Delete the folder if is_delete is True
    if is_delete:
        shutil.rmtree(folder)

    # Debug print final
    ARCHIVE_DEBUG and print(Fore.GREEN + '='*70 + Style.RESET_ALL)

def archive_folder_process(process_obj):
    archive_folder(process_obj["folder"], process_obj["is_delete"])
