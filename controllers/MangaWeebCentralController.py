import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from pprint import pprint

from common.Constants import WEBCENTRAL_DEBUG
from common.Commons import generate_filename
DEBUG_OBJ = {
    "get_link_chapter_weebcentral": False,
    "get_list_image_weebcentral": False,
}

def get_link_chapter_weebcentral(link: str, num_chap = -1, start_idx = -1) -> str:
    """
    Generate chapter link from server weebcentral.com
    :param link: link to get list of chapters
    :param num_chap: number of chapters to get
    :param start_idx: start index of the chapter
    :return: list of chapters
    """
    
    # Debug print initial
    if WEBCENTRAL_DEBUG and DEBUG_OBJ["get_link_chapter_weebcentral"]:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'MangaWeebCentralController: get_link_chapter_weebcentral'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"Link:":<20}' + Style.RESET_ALL + f'{link: >49}')
        print(Fore.BLUE + f'{"Num chap:":<20}' + Style.RESET_ALL + f'{num_chap: >49}')
        print(Fore.BLUE + f'{"Start idx:":<20}' + Style.RESET_ALL + f'{start_idx: >49}')

    id_manga = link.split('/')[-2]

    link_list_chapters = f"https://weebcentral.com/series/{id_manga}/full-chapter-list"

    try:
        response = requests.get(link_list_chapters, headers={
            'User-agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the list of chapters. Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')

        link_a = soup.find_all('a')
        list_chapters = [link.get('href') for link in link_a if link.get('href') and link.get('href').startswith('https')]

        if start_idx != -1:
            list_chapters = list_chapters[::-1]
            list_chapters = list_chapters[start_idx:]
            
        if num_chap != -1:
            list_chapters = list_chapters[:num_chap]
            
        if start_idx == -1:
            list_chapters = list_chapters[::-1]
        
        # Debug print list_chapters
        if WEBCENTRAL_DEBUG and DEBUG_OBJ["get_link_chapter_weebcentral"]:
            print(Fore.CYAN + f'{"List chapters:":<20}' + Style.RESET_ALL)
            pprint(list_chapters)
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

        return "https://weebcentral.com/", list_chapters

    except Exception as e:
        if WEBCENTRAL_DEBUG and DEBUG_OBJ["get_link_chapter_weebcentral"]:
            print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{e: >49}')
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)


def get_list_image_weebcentral(link: str) -> str:
    """
    Get list of images from server weebcentral.com
    :param link: link to get list of images
    :return: list of images
    """

    if WEBCENTRAL_DEBUG and DEBUG_OBJ["get_list_image_weebcentral"]:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'MangaWeebCentralController: get_list_image_weebcentral'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"Link:":<20}' + Style.RESET_ALL + f'{link: >49}')

    try:
        response = requests.get(link, headers={
            'User-agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the list of images. Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get total images in chapter
        chapter_total_images = soup.find_all('button', class_='w-full btn')
        chapter_total_images = len(chapter_total_images)

        # Sample image 
        img_link_element = soup.find('link', rel='preload')
        img_link = img_link_element.get('href')

        server_img = img_link.split('/')
        format_img = server_img.pop()
        image_server = '/'.join(server_img)

        extension_img = format_img.split('.')[-1]
        tmp_image_file = format_img.replace(f'.{extension_img}', '')
        chapter_number = tmp_image_file.split('-')[0]

        list_images = []
        for idx in range(1, chapter_total_images+1):
            img_link = f"{image_server}/{chapter_number}-{generate_filename(idx=idx,str_len=3)}.{extension_img}"
            list_images.append(img_link)

        chap_name = f"Chapter {chapter_number}"

        # Debug print final
        if WEBCENTRAL_DEBUG and DEBUG_OBJ["get_list_image_weebcentral"]:
            print(Fore.CYAN + f'{"Chapter name:":<20}' + Style.RESET_ALL + f'{chap_name: >49}' )
            print(Fore.CYAN + f'{"List images:":<20}' + Style.RESET_ALL)
            pprint(list_images)
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

        return chap_name, list_images
    
    except Exception as e:
        if WEBCENTRAL_DEBUG and DEBUG_OBJ["get_list_image_weebcentral"]:
            print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{e: >49}')
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
