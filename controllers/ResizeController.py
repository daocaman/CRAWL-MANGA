import os
from PIL import Image

from common.Commons import is_image_file
from common.Constants import RESIZE_DEBUG
from common.Constants import verticle_size, horizontal_size
from common.Messages import log_start_function, log_parameter, END_LOG, log_error
from common.Messages import MSG_ERR_CONTROLLER_RESIZE
from common.Validations import check_and_create_folder

def resize_image(folder: str='', is_horizontal: bool = False):
    """
    Resize images in a folder
    :param folder: folder to resize images
    :param is_horizontal: resize images horizontally
    :return: None
    """

    # Debug print initial
    if RESIZE_DEBUG:
        log_start_function("ResizeController", "resize_image")
        log_parameter("Folder", folder, 1)
        log_parameter("Is horizontal", is_horizontal, 1)
        
    try:
        
        check_and_create_folder(folder, alert=True)
        
        image_files = [f for f in os.listdir(folder) if is_image_file(f)]
        
        for  f in image_files:

            new_size = verticle_size
            
            image = Image.open(os.path.join(folder, f))

            width, height = image.size
            
            # Debug print width and height
            RESIZE_DEBUG and log_parameter("Old size", f'{width}x{height}', 2)
            
            # Check if the image is horizontal
            if width > height or is_horizontal:
                new_size = horizontal_size
            
            # Debug print new size
            RESIZE_DEBUG and log_parameter("New size", new_size, 2)

            resized_image = image.resize(new_size)
            resized_image.convert("RGB").save(os.path.join(folder, f))

        # Debug print final
        RESIZE_DEBUG and print(END_LOG)
        
    except Exception as e:
        if RESIZE_DEBUG:
            log_error("ResizeController", "resize_image", e)
        raise Exception(MSG_ERR_CONTROLLER_RESIZE.format(e))

def resize_image_process(resize_obj):
    """
    Process resize images
    :param resize_obj: Resize object
    :return: None
    """
    resize_image(resize_obj["folder"], resize_obj["is_horizontal"])
