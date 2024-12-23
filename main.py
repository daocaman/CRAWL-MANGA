from art import *
import questionary

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
from common.Constant_v1_1 import main_menu, radio_menu


def main():
    title = text2art("Crawl Manga Tool", "standard")

    print(title)
    while True:
        print(f'Please select the option you want to do {art("energy")}: ')

        menu_options = main_menu

        choose_task = questionary.select("Select main task: ", menu_options).ask()

        task_index = menu_options.index(choose_task)

        if task_index == 0:
            quest_form_download_manga()
        elif task_index == 1:   
            quest_form_create_metadata()
        elif task_index == 2:
            quest_form_archive_folders()
        elif task_index == 3:
            quest_form_download_cover()
        elif task_index == 4:
            quest_form_resize_images()
        elif task_index == 5:
            quest_form_download_yt()
        elif task_index == 6:
            quest_form_reformat()
        elif task_index == 7:
            quest_form_rename_files()
        elif task_index == 8:
            quest_form_move_chap_vol()
        elif task_index == 9:
            quest_form_create_list_file()
        elif task_index == 10:
            quest_form_rename_with_file()
        elif task_index == 11:
            quest_form_download_m3u8()

        continue_task = questionary.select("Do you want to continue? ", radio_menu).ask()
        continue_task_index = radio_menu.index(continue_task)
        
        if continue_task_index == 0:
            break

if __name__ == "__main__":
    main()

