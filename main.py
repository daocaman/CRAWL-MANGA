from art import *

from quest.DownloadManga import quest_form_download_manga
from quest.CreateMeta import quest_form_create_metadata
from quest.DownloadCovers import quest_form_download_cover
from quest.ArchiveFolders import quest_form_archive_folders
from quest.ResizeImages import quest_form_resize_images
from quest.DownloadYT import quest_form_download_yt
from quest.Reformat import quest_form_reformat
from quest.RenameFiles import quest_form_rename_files
from quest.MoveChapVol import quest_form_move_chap_vol
from quest.CreateListFile import quest_form_create_list_file
from quest.RenameWithFile import quest_form_rename_with_file
from quest.DownloadM3U8 import quest_form_download_m3u8
from quest.ConvertTS import quest_form_convert_ts
from common.Constant_v1_1 import main_menu, manga_options_menu, video_menu, rename_list_menu
from common.QuestCommon import select_question, yes_no_question

def main():
    title = text2art("Crawl Manga Tool", "standard")

    print(title)
    while True:
        print(f'Please select the option you want to do {art("energy")}: ')

        menu_options = main_menu

        task_index = select_question("Select main task: ", menu_options)
        
        if task_index == 0:
            manga_task_index = select_question("Select manga task: ", manga_options_menu)
            if manga_task_index == 0:
                quest_form_download_manga()
            elif manga_task_index == 1:
                quest_form_create_metadata()
            elif manga_task_index == 2:
                quest_form_archive_folders()
            elif manga_task_index == 3:
                quest_form_download_cover()
            elif manga_task_index == 4:
                quest_form_resize_images()
            elif manga_task_index == 5:
                quest_form_reformat()
            elif manga_task_index == 6:
                quest_form_move_chap_vol()
        elif task_index == 1:
            video_task_index = select_question("Select video task: ", video_menu)
            if video_task_index == 0:
                quest_form_download_yt()
            elif video_task_index == 1:
                quest_form_download_m3u8()
            elif video_task_index == 2:
                quest_form_convert_ts()
        elif task_index == 2:
            rename_list_task_index = select_question("Select rename list task: ", rename_list_menu)
            if rename_list_task_index == 0:
                quest_form_rename_files()
            elif rename_list_task_index == 1:
                quest_form_create_list_file()
            elif rename_list_task_index == 2:
                quest_form_rename_with_file()
                
        is_continue = yes_no_question("Do you want to continue? ")
        if not is_continue:
            break

if __name__ == "__main__":
    main()

