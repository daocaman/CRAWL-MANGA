from colorama import Fore, Style
from pprint import pprint

START_LOG =  Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL
END_LOG = Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL

def log_start_function(controller: str, function_name: str):
    """
    Log the start of a function
    :param controller: controller name
    :param function_name: function name
    :return: None
    """
    print(START_LOG)
    print(Fore.YELLOW + f'{controller}: {function_name}'.center(70) + Style.RESET_ALL)

def log_parameter(var_name: str, var_value, var_type: int = 1):
    """
    Log a parameter
    :param var_name: parameter name
    :param var_value: parameter value
    :param var_type: parameter type (1: input_param, 2: debug_param)
    :return: None
    """
    try:
        if var_type == 1:
            print(Fore.BLUE + f'{var_name:<20}' + Style.RESET_ALL + f'{var_value: >49}')
        elif var_type == 2:
            print(Fore.CYAN + f'{var_name:<20}' + Style.RESET_ALL + f'{var_value: >49}')
    except Exception as e:
        if var_type == 1:
            print(Fore.BLUE + f'{var_name:<20}' + Style.RESET_ALL)
            pprint(var_value)
        elif var_type == 2:
            print(Fore.CYAN + f'{var_name:<20}' + Style.RESET_ALL)
            pprint(var_value)
 
def log_error(controller: str, function_name: str, error, log_end: bool = True):
    """
    Log an error
    :param controller: controller name
    :param function_name: function name
    :param error: error object
    :param log_end: log the end of the function
    :return: None
    """
    print(Fore.RED + f'Error in {controller}: {function_name}'+ Style.RESET_ALL)
    pprint(error)
    if log_end:
        print(END_LOG)
        
MSG_ERR_DOWN_IMG = "Error download image at trial {0}!f"
MSG_ERR_FILE_NOT_EXIST = "File <{0}> is not found!"
MSG_ERR_FOLDER_NOT_EXIST = "Folder <{0}> is not found!"
MSG_ERR_URL_NOT_VALID_VIDEO = "URL is not a valid YouTube video URL!"
MSG_ERR_URL_NOT_VALID_PLAYLIST = "URL is not a valid YouTube playlist URL!"
MSG_ERR_REQUEST_FAILED = "Failed to fetch the list of chapters with status code {0}!"
MSG_ERR_NO_FOLDERS_WITH_NAME = "No folders found with name <{0}>!"
MSG_ERR_NO_COVERS_FOUND = "No covers found!"
MSG_ERR_NO_MANGA_TITLE = "No manga title found!"

MSG_ERR_CONTROLLER_ARCHIVE = "Error in ArchiveController: {0}!"
MSG_ERR_CONTROLLER_CONVERT_TS = "Error in ConvertTSController: {0}!"
MSG_ERR_CONTROLLER_DOWNLOAD_COVER = "Error in DownloadCoverController: {0}!"
MSG_ERR_CONTROLLER_DOWNLOAD_M3U8 = "Error in DownloadM3U8Controller: {0}!"
MSG_ERR_CONTROLLER_DOWNLOAD_YOUTUBE = "Error in DownloadYoutubeController: {0}!"
MSG_ERR_CONTROLLER_LIST_AND_RENAME = "Error in ListAndRenameController: {0}!"
MSG_ERR_CONTROLLER_MANGASEE = "Error in MangaMangaseeController: {0}!"
MSG_ERR_CONTROLLER_NETTRUYEN = "Error in MangaNettruyenController: {0}!"
MSG_ERR_CONTROLLER_WEEBCENTRAL = "Error in MangaWeebCentralController: {0}!"
MSG_ERR_CONTROLLER_METADATA = "Error in MetadataController: {0}!"
MSG_ERR_CONTROLLER_MOVE_CHAP_VOL = "Error in MoveChapController: {0}!"
MSG_ERR_CONTROLLER_REFORMAT = "Error in ReformatController: {0}!"
MSG_ERR_CONTROLLER_RESIZE = "Error in ResizeController: {0}!"
