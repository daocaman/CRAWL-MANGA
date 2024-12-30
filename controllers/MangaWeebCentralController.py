import requests
from bs4 import BeautifulSoup

from common.Commons import generate_filename
from common.Constants import header_obj
from common.Constants import WEEBCENTRAL_DEBUG, link_chapter_weebcentral, server_weebcentral
from common.Messages import MSG_ERR_REQUEST_FAILED, MSG_ERR_CONTROLLER_WEEBCENTRAL
from common.Messages import log_start_function, log_parameter, log_error, END_LOG

DEBUG_OBJ = {
    "get_link_chapter_weebcentral": True,
    "get_list_image_weebcentral": True,
}

def get_link_chapter_weebcentral(link: str, num_chap: int = -1, start_idx: int = -1):
    """
    Generate chapter link from server weebcentral.com
    :param link: link to get list of chapters
    :param num_chap: number of chapters to get
    :param start_idx: start index of the chapter
    :return: list of chapters
    """
    
    # Debug print initial
    if WEEBCENTRAL_DEBUG and DEBUG_OBJ["get_link_chapter_weebcentral"]:
        log_start_function("MangaWeebCentralController", "get_link_chapter_weebcentral")
        log_parameter("Link", link, 1)
        log_parameter("Num chap", num_chap, 1)
        log_parameter("Start idx", start_idx, 1)
        
    id_manga = link.split('/')[-2]

    link_list_chapters = link_chapter_weebcentral.format(id_manga)
    
    if WEEBCENTRAL_DEBUG and DEBUG_OBJ["get_link_chapter_weebcentral"]:
        log_parameter("Link list chapters", link_list_chapters, 1)

    try:
        response = requests.get(link_list_chapters, headers=header_obj)
        if response.status_code != 200:
            raise Exception(MSG_ERR_REQUEST_FAILED.format(response.status_code))
       
        soup = BeautifulSoup(response.text, 'html.parser')

        link_a = soup.find_all('a')
        list_chapters = [link.get('href') for link in link_a if link.get('href') and link.get('href').startswith('http')]

        if start_idx != -1:
            list_chapters = list_chapters[::-1]
            list_chapters = list_chapters[start_idx:]

        if num_chap != -1:
            list_chapters = list_chapters[:num_chap]
            
        if start_idx == -1:
            list_chapters = list_chapters[::-1]
        
        # Debug print list_chapters
        if WEEBCENTRAL_DEBUG and DEBUG_OBJ["get_link_chapter_weebcentral"]:
            log_parameter("List chapters", list_chapters, 2)
            print(END_LOG)

        return (server_weebcentral, list_chapters)

    except Exception as e:
        if WEEBCENTRAL_DEBUG and DEBUG_OBJ["get_link_chapter_weebcentral"]:
            log_error("MangaWeebCentralController", "get_link_chapter_weebcentral", e)
        raise Exception(MSG_ERR_CONTROLLER_WEEBCENTRAL.format("get_link_chapter_weebcentral"))


def get_list_image_weebcentral(link: str):
    """
    Get list of images from server weebcentral.com
    :param link: link to get list of images
    :return: list of images
    """

    if WEEBCENTRAL_DEBUG and DEBUG_OBJ["get_list_image_weebcentral"]:
        log_start_function("MangaWeebCentralController", "get_list_image_weebcentral")
        log_parameter("Link", link, 1)

    try:
        response = requests.get(link, headers=header_obj)
        if response.status_code != 200:
            raise Exception(MSG_ERR_REQUEST_FAILED.format(response.status_code))
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
        if WEEBCENTRAL_DEBUG and DEBUG_OBJ["get_list_image_weebcentral"]:
            log_parameter("Chapter name", chap_name, 2)
            log_parameter("List images", list_images, 2)
            print(END_LOG)

        return chap_name, list_images
    
    except Exception as e:
        if WEEBCENTRAL_DEBUG and DEBUG_OBJ["get_list_image_weebcentral"]:
            log_error("MangaWeebCentralController", "get_list_image_weebcentral", e)
        raise Exception(MSG_ERR_CONTROLLER_WEEBCENTRAL.format("get_list_image_weebcentral"))
