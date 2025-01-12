import requests
from bs4 import BeautifulSoup

from common.Commons import generate_filename
from common.Constants import NETTRUYEN_DEBUG, prefix_chapter_folder
from common.Constants import header_obj, timeout_obj
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_CONTROLLER_NETTRUYEN

DEBUG_OBJ = {
    "get_link_chapter_nettruyen": True,
    "get_list_image_nettruyen": True,
}

nettruyen_req_headers = header_obj.copy()

def get_link_chapter_nettruyen(link: str = '', num_chap: int = -1, start_idx: int = -1):
    """
    Get list of chapters from nettruyen
    :param link: link to get list of chapters
    :param num_chap: number of chapters to get
    :param start_idx: start index of the chapter
    :return: list of chapters
    """
    
    # Debug print initial
    if NETTRUYEN_DEBUG and DEBUG_OBJ["get_link_chapter_nettruyen"]:
        log_start_function("MangaNettruyenController", "get_link_chapter_nettruyen")
        log_parameter("Link", link, 1)
        log_parameter("Num chap", num_chap, 1)
        log_parameter("Start idx", start_idx, 1)
      
    list_chapters = []
    link_splits = link.split('/')
    server = '/'.join(link_splits[:3])

    container_chapters = "nt_listchapter"
    ul_id = "desc"
    

    try:
        r = requests.get(link, headers=nettruyen_req_headers, timeout=timeout_obj)
        
        htmlSource = r.content
        soup = BeautifulSoup(htmlSource, 'html.parser')

        container_chapters_ele = soup.find(id=container_chapters)
        ul_ele = container_chapters_ele.find(id=ul_id)
        a_eles = ul_ele.find_all('a')

        list_chapters = [a['href'] for a in a_eles]
        
        if start_idx != -1:
            list_chapters = list_chapters[::-1]
            list_chapters = list_chapters[start_idx:]
            
        if num_chap != -1:
            list_chapters = list_chapters[:num_chap]
            
        if start_idx == -1:
            list_chapters = list_chapters[::-1]

        # Debug print list_chapters
        if NETTRUYEN_DEBUG and DEBUG_OBJ["get_link_chapter_nettruyen"]:
            log_parameter("List chapters", list_chapters, 2)

        # Debug print final
        NETTRUYEN_DEBUG and DEBUG_OBJ["get_link_chapter_nettruyen"] and print(END_LOG)

        return (server, list_chapters)
        
    except Exception as e:
        if NETTRUYEN_DEBUG and DEBUG_OBJ["get_link_chapter_nettruyen"]:
            log_error("MangaNettruyenController", "get_link_chapter_nettruyen", e)
        raise Exception(MSG_ERR_CONTROLLER_NETTRUYEN.format("get_link_chapter_nettruyen"))
    

def get_list_image_nettruyen(link: str = ''):
    """
    Get list of images from nettruyen
    :param link: link to get list of images
    """
    
    # Debug print initial
    if NETTRUYEN_DEBUG and DEBUG_OBJ["get_list_image_nettruyen"]:
        log_start_function("MangaNettruyenController", "get_list_image_nettruyen")
        log_parameter("Link", link, 1)

    list_images = []
    
    title = "Not found"
    
    image_src_atrs = ["data-src", "data-sv1", "data-sv2"]

    div_images = ["page-chapter"]

    try:
        r = requests.get(link, headers=nettruyen_req_headers, timeout=timeout_obj)
        
        htmlSource = r.content
        soup = BeautifulSoup(htmlSource, 'html.parser')

        title = soup.find('title')

        title = title.text.split(" Next Chap ")[0].strip()

        chap = title.split(" ")[-1]
        odd = -1
        if len(chap.split(".")) >= 2:
            odd = chap.split(".")[-1]
            chap = chap.split(".")[0]

        title = f"{prefix_chapter_folder} {generate_filename(idx=int(chap))}"

        if odd != -1:
            title = f"{title}.{odd}"

        div_images_ele = []
        for div_image in div_images:
            div_images_ele = soup.find_all('div', class_=div_image)
            if len(div_images_ele) > 0:
                break
        
        for div_image_ele in div_images_ele:
            img_ele = div_image_ele.find('img')
            for atr in image_src_atrs:
                if atr in img_ele.attrs:
                    list_images.append(img_ele[atr])
                    break

        list_images = [f if 'https' in f else "https://" + f  for f in list_images ]

        # Debug print list_images
        if NETTRUYEN_DEBUG and DEBUG_OBJ["get_list_image_nettruyen"]:
            log_parameter("List images", list_images, 2)
            print(END_LOG)

        return (title, list_images)
        
    except Exception as e:
        if NETTRUYEN_DEBUG and DEBUG_OBJ["get_list_image_nettruyen"]:
            log_error("MangaNettruyenController", "get_list_image_nettruyen", e)
        raise Exception(MSG_ERR_CONTROLLER_NETTRUYEN.format("get_list_image_nettruyen"))
    
