from common.Commons import download_image

def download_image_process(image_obj):
    code_result = download_image(
                    link=image_obj["link"], 
                    server=image_obj["server"], 
                    file=image_obj["file"]
                )
    return code_result
