import os
import json

from common.Constants import LIST_AND_RENAME_DEBUG, file_rename_list, folder_running_resource
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_CONTROLLER_LIST_AND_RENAME
from common.Validations import check_and_create_folder, check_file_exist

DEBUG_OBJ = {
    "get_list_of_files": LIST_AND_RENAME_DEBUG,
    "rename_file": LIST_AND_RENAME_DEBUG,
}

def get_list_of_files(path):
    """
    Get list of files in the given path and save to a JSON file.
    :param path: The path to get the list of files.
    :return: None
    """
    if LIST_AND_RENAME_DEBUG and DEBUG_OBJ["get_list_of_files"]:
        log_start_function("ListAndRenameController", "get_list_of_files")
        log_parameter("Folder path", path, 1)

    try:
        check_and_create_folder(path, True)

        files = [f.encode('utf-8').decode('utf-8') for f in os.listdir(path)]
        file_objs = []
        for file in files:
            file_obj = {
                "root_path": path,
                "current_file_name": file,
                "new_file_name": file,
            }
            file_objs.append(file_obj)
            
        if LIST_AND_RENAME_DEBUG and DEBUG_OBJ["get_list_of_files"]:
            log_parameter("List object files", file_objs, 2)
            print(END_LOG)
        
        with open(f'{folder_running_resource}/{file_rename_list}', "w+", encoding="utf-8") as f:
            json.dump(file_objs, f, indent=2, ensure_ascii=False)
            
        print(END_LOG)
    except Exception as e:
        if LIST_AND_RENAME_DEBUG and DEBUG_OBJ["get_list_of_files"]:
            log_error("ListAndRenameController", "get_list_of_files", e)
        raise Exception(MSG_ERR_CONTROLLER_LIST_AND_RENAME.format("get_list_of_files"))
        
def rename_file():
    """
    Rename the file with the given filename.
    :return: None
    """
    
    if LIST_AND_RENAME_DEBUG and DEBUG_OBJ["rename_file"]:
        log_start_function("ListAndRenameController", "rename_file")
    
    try:

        check_file_exist(f'{folder_running_resource}/{file_rename_list}')
        
        with open(file_rename_list, "r", encoding="utf-8") as f:
            file_objs = json.load(f)
            
        for file_obj in file_objs:
            os.rename(os.path.join(file_obj["root_path"], file_obj["current_file_name"]), os.path.join(file_obj["root_path"], file_obj["new_file_name"]))
            
        if LIST_AND_RENAME_DEBUG and DEBUG_OBJ["rename_file"]:
            log_parameter("List object files", file_objs, 2)
            print(END_LOG)
    except Exception as e:
        if LIST_AND_RENAME_DEBUG and DEBUG_OBJ["rename_file"]:
            log_error("ListAndRenameController", "rename_file", e)
        raise Exception(MSG_ERR_CONTROLLER_LIST_AND_RENAME.format("rename_file"))
    
        