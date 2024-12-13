import os
from PIL import Image
from colorama import Fore, Style
from common.Constants import RESIZE_DEBUG
from common.Constants import verticle_size, horizontal_size
from common.Commons import is_image_file

def resize_image(folder='', is_horizontal=False):
    """
    Resize images in a folder
    :param folder: folder to resize images
    :param is_horizontal: resize images horizontally
    :return: None
    """

    # Debug print initial
    RESIZE_DEBUG and print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
    RESIZE_DEBUG and print(Fore.YELLOW + 'ResizeController: resize_image'.center(70) + Style.RESET_ALL)
    RESIZE_DEBUG and print(Fore.BLUE + f'{"Folder:":<20}' + Style.RESET_ALL + f'{folder: >49}')
    RESIZE_DEBUG and print(Fore.BLUE + f'{"Is horizontal:":<20}' + Style.RESET_ALL + f'{str(is_horizontal): >49}')


    image_files = [f for f in os.listdir(folder) if is_image_file(f)]
    
    for  f in image_files:

        new_size = verticle_size
        
        image = Image.open(os.path.join(folder, f))

        width, height = image.size
        
        # Debug print width and height
        RESIZE_DEBUG and print(Fore.CYAN + f'{"Old size:":<20}' + Style.RESET_ALL + f'{width}x{height}')
        
        # Check if the image is horizontal
        if width > height or is_horizontal:
            new_size = horizontal_size
        
        # Debug print new size
        RESIZE_DEBUG and print(Fore.CYAN + f'{"New size:":<20}' + Style.RESET_ALL + f'{new_size}')

        resized_image = image.resize(new_size)
        resized_image.save(os.path.join(folder, f))

    # Debug print final
    RESIZE_DEBUG and print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

def resize_image_process(resize_obj):
    resize_image(resize_obj["folder"], resize_obj["is_horizontal"])
