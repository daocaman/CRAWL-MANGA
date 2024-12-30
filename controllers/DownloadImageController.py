from common.Commons import download_image

def download_image_process(image_obj):
    """
    Process the download image
    :param image_obj: image object
    :return: download result code
    """
    code_result = download_image(
                    link=image_obj["link"], 
                    server=image_obj["server"], 
                    file=image_obj["file"]
                )
    return code_result
