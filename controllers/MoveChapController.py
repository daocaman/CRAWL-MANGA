
import os
import shutil
import json

from common.Commons import generate_filename, is_image_file, extract_number
from common.Constants import MOVE_CHAP_VOL_DEBUG, prefix_chapter_folder, prefix_image_file, file_chapters
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_CONTROLLER_MOVE_CHAP_VOL
from common.Validations import check_and_create_folder

def move_chap_vol(target_folder: str, start_chap: int = -1, end_chap: int = -1, delete_chap_folder: bool = False):
    try:
        if MOVE_CHAP_VOL_DEBUG:
            log_start_function("MoveChapController", "move_chap_vol")
            log_parameter("Target folder", target_folder, 1)
            log_parameter("Start chapter", start_chap, 1)
            log_parameter("End chapter", end_chap, 1)
            log_parameter("Delete chapter folder", delete_chap_folder, 1)
            
        check_and_create_folder(target_folder)
            
        chapters_folder_validation = []
            
        for i in range(start_chap, end_chap + 1):
            tmp_chap_folder = f'{prefix_chapter_folder} {generate_filename(idx=int(i))}'
            check_and_create_folder(tmp_chap_folder, True)
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
                new_name = generate_filename(prefix_image_file, count, ".jpg")
                shutil.copy(os.path.join(chap_folder, img),
                            os.path.join(target_folder, new_name))
                count += 1
                
            if delete_chap_folder:
                shutil.rmtree(chap_folder)
                
         # Write the list of chapters to the file
        with open(os.path.join(target_folder, file_chapters), 'w+', encoding="utf-8") as json_file:
            # Write the list to the file
            json.dump(list_chapters, json_file, ensure_ascii=False, indent=4)
            
        MOVE_CHAP_VOL_DEBUG and print(END_LOG)
        
    except Exception as e:
        if MOVE_CHAP_VOL_DEBUG:
            log_error("MoveChapController", "move_chap_vol", e)
        raise Exception(MSG_ERR_CONTROLLER_MOVE_CHAP_VOL.format(e))
