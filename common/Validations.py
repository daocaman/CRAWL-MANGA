import os

from common.Messages import MSG_ERR_FOLDER_NOT_EXIST, MSG_ERR_FILE_NOT_EXIST, MSG_ERR_NO_FOLDERS_WITH_NAME
from common.Messages import MSG_ERR_URL_NOT_VALID_VIDEO, MSG_ERR_URL_NOT_VALID_PLAYLIST
from common.Constants import link_yt_video, link_yt_playlist

def check_and_create_folder(folder_path: str, alert: bool = False, create: bool = False):
    """
    Check and create folder. If alert is True, raise an exception when the folder does not exist, else create the folder
    :param folder_path: path to the folder
    :param alert: alert if the folder does not exist
    :param create: create the folder if it does not exist
    :return: None
    """
    if not os.path.exists(folder_path):
        if alert:
            raise Exception(MSG_ERR_FOLDER_NOT_EXIST.format(folder_path))
        elif create:
            os.makedirs(folder_path)
        else:
            return False
            
    return True

def check_file_exist(file_path: str, alert: bool = True):
    """
    Check if the file exists
    :param file_path: path to the file
    :param alert: alert if the file does not exist
    :return: None
    """
    if not os.path.exists(file_path):
        if alert:
            raise Exception(MSG_ERR_FILE_NOT_EXIST.format(file_path))
        else:
            return False
        
    return True

def check_and_get_list_of_folders(contain_name: str = "", alert: bool = True):
    """
    Get list of folders in the given folder path
    :param contain_name: name to contain in the folder
    :param alert: alert if the folder does not exist
    :return: list of folders
    """
    folders = os.listdir()
    folders = [f for f in folders if os.path.isdir(f) and contain_name in f]
    
    if len(folders) == 0 and alert:
        raise Exception(MSG_ERR_NO_FOLDERS_WITH_NAME.format(contain_name))
    
    return folders

def check_valid_video_url(url: str, alert: bool = True):
    """
    Check if the URL is a valid YouTube video URL
    :param url: URL to check
    :param alert: alert if the URL is not valid
    :return: None
    """
    if not url.startswith(link_yt_video):
        if alert:
            raise Exception(MSG_ERR_URL_NOT_VALID_VIDEO)
        else:
            return False
    
    return True

def check_valid_playlist_url(url: str, alert: bool = True):
    """
    Check if the URL is a valid YouTube playlist URL
    :param url: URL to check
    :param alert: alert if the URL is not valid
    :return: None
    """
    if not url.startswith(link_yt_playlist):
        if alert:
            raise Exception(MSG_ERR_URL_NOT_VALID_PLAYLIST)
        else:
            return False
    
    return True
