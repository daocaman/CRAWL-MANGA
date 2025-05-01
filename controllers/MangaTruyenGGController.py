from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from common.Commons import generate_filename
from common.Constants import max_length_idx
from common.Constants import TRUYENGG_DEBUG, server_truyengg
from common.Messages import MSG_ERR_CONTROLLER_TRUYENGG
from common.Messages import log_start_function, log_parameter, log_error, END_LOG

DEBUG_OBJ = {
    "get_link_chapter_truyengg": True,
    "get_list_image_truyengg": True,
}

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

def get_link_chapter_truyengg(link: str, num_chap: int = -1, start_idx: int = -1):
    """
    Generate chapter link from server truyengg.com
    :param link: link to get list of chapters
    :param num_chap: number of chapters to get
    :param start_idx: start index of the chapter
    :return: list of chapters
    """
    
    # Debug print initial
    if TRUYENGG_DEBUG and DEBUG_OBJ["get_link_chapter_truyengg"]:
        log_start_function("MangaTruyenGGController", "get_link_chapter_truyengg")
        log_parameter("Link", link, 1)
        log_parameter("Num chap", num_chap, 1)
        log_parameter("Start idx", start_idx, 1)

    try:

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Execute CDP commands to prevent detection
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })

        driver.get(link)

        list_chapters = driver.find_elements(By.XPATH, '//ul[@class="list_chap"]//a')

        list_chapters = [chapter.get_attribute('href') for chapter in list_chapters if chapter.get_attribute('href') and chapter.get_attribute('href').startswith('http')]

        if start_idx != -1:
            list_chapters = list_chapters[::-1]
            list_chapters = list_chapters[start_idx:]

        if num_chap != -1:
            list_chapters = list_chapters[:num_chap]
            
        if start_idx == -1:
            list_chapters = list_chapters[::-1]
        
        # Debug print list_chapters
        if TRUYENGG_DEBUG and DEBUG_OBJ["get_link_chapter_truyengg"]:
            log_parameter("List chapters", list_chapters, 2)
            print(END_LOG)

        driver.close()

        return (server_truyengg, list_chapters)

    except Exception as e:
        if TRUYENGG_DEBUG and DEBUG_OBJ["get_link_chapter_truyengg"]:
            log_error("MangaTruyenGGController", "get_link_chapter_truyengg", e)
        raise Exception(MSG_ERR_CONTROLLER_TRUYENGG.format("get_link_chapter_truyengg"))


def get_list_image_truyengg(link: str):
    """
    Get list of images from server truyengg.com
    :param link: link to get list of images
    :return: list of images
    """

    if TRUYENGG_DEBUG and DEBUG_OBJ["get_list_image_truyengg"]:
        log_start_function("MangaTruyenGGController", "get_list_image_truyengg")
        log_parameter("Link", link, 1)

    try:

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Execute CDP commands to prevent detection
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })

        chapter_number = link.split('-chap-')[-1].split('.')[0]

        log_parameter("Chapter number", chapter_number, 2)

        chapter_number = generate_filename(idx=int(chapter_number), str_len=max_length_idx)

        driver.get(link)

        list_images = driver.find_elements(By.XPATH, '//div[contains(@class, "content_detail_manga")]//img')

        list_images = [image.get_attribute('src') for image in list_images if image.get_attribute('src') and image.get_attribute('src').startswith('http')]

        chap_name = f"Chapter {chapter_number}"

        # Debug print final
        if TRUYENGG_DEBUG and DEBUG_OBJ["get_list_image_truyengg"]:
            log_parameter("Chapter name", chap_name, 2)
            log_parameter("List images", list_images, 2)
            print(END_LOG)

        return chap_name, list_images
    
    except Exception as e:
        if TRUYENGG_DEBUG and DEBUG_OBJ["get_list_image_truyengg"]:
            log_error("MangaTruyenGGController", "get_list_image_truyengg", e)
        raise Exception(MSG_ERR_CONTROLLER_TRUYENGG.format("get_list_image_truyengg"))
