
from colorama import Fore, Style
import os
import shutil
import json
from common.Constants import MOVE_CHAP_VOL_DEBUG, chapter_folder_prefix, file_prefix, file_chapters
from common.Commons import generate_filename, is_image_file, extract_number


def move_chap_vol(target_folder, start_chap, end_chap, delete_chap_folder):
    try:
        if MOVE_CHAP_VOL_DEBUG:
            print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)
            print(Fore.YELLOW + 'MoveChapController: move_chap_vol'.center(70) + Style.RESET_ALL)
            
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
            
        chapters_folder_validation = []
            
        for i in range(start_chap, end_chap + 1):
            tmp_chap_folder = f'{chapter_folder_prefix} {generate_filename(idx=int(i))}'
            print(tmp_chap_folder)
            if not os.path.exists(tmp_chap_folder):
                raise Exception(f"Chapter folder {tmp_chap_folder} not found")
            
            chapters_folder_validation.append(tmp_chap_folder)
            
        list_chapters = []
        count = 1
        
        for chap_folder in chapters_folder_validation:
            list_chapters.append({
                "title": chap_folder,
                "page": count
            })
            images = os.listdir(chap_folder)
            images = [f for f in images if is_image_file(f)]
            images = sorted(images, key=lambda x: extract_number(x, is_float=True))
            
            for img in images:
                new_name = generate_filename(file_prefix, count, ".jpg")
                shutil.copy(os.path.join(chap_folder, img),
                            os.path.join(target_folder, new_name))
                count += 1
                
            if delete_chap_folder:
                shutil.rmtree(chap_folder)
                
         # Write the list of chapters to the file
        with open(os.path.join(target_folder, file_chapters), 'w+', encoding="utf-8") as json_file:
            # Write the list to the file
            json.dump(list_chapters, json_file, ensure_ascii=False, indent=4)
            
        if MOVE_CHAP_VOL_DEBUG:
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
        
    except Exception as e:
        if MOVE_CHAP_VOL_DEBUG:
            print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
    
