from art import *
from common.Constants import main_menu, manga_menu
import questionary
from quest.DownloadManga import quest_form_download_manga


def main():
    title = text2art("Crawl Manga Tool", "standard")

    print(title)
    print(f'Please select the option you want to do {art("energy")}: ')

    menu_options = main_menu

    choose_task = questionary.select("Select main task: ", menu_options).ask()

    task_index = menu_options.index(choose_task)

    if task_index == 0:
        manga_link, server, number_of_chapter, start_from_index = quest_form_download_manga()
        quest_download_manga(manga_link, server, number_of_chapter, start_from_index)
    


if __name__ == "__main__":
    main()

