import os
from colorama import Fore, Style
from pprint import pprint

from common.Constants import METADATA_DEBUG, file_comic_xml, comic_xml, comic_series, comic_writer, comic_volume, comic_summary, comic_page, comic_pages_op, comic_pages_cl
from common.Messages import MSG_ERR_CONTROLLER_METADATA
from common.Messages import log_start_function, log_parameter, log_error, END_LOG

def generate_metadata(series: str, writer: str, vol: int = -1, table_content: list = [], summary: str = "", target_folder: str = ""):
    """
    Generate metadata for a comic
    :param series: Series of the comic
    :param writer: Writer of the comic
    :param vol: Volume of the comic
    :param table_content: Table content of the comic
    :param summary: Summary of the comic
    :param target_folder: Target folder to save the metadata file
    :return: None
    """

    # Debug print initial
    if METADATA_DEBUG:
        log_start_function("MetadataController", "generate_metadata")
        log_parameter("Series", series, 1)
        log_parameter("Writer", writer, 1)
        log_parameter("Volume", vol, 1)
        log_parameter("Table content", table_content, 1)
        log_parameter("Summary", summary, 1)
        log_parameter("Target folder", target_folder, 1)
        
    try:
        xml_containt = comic_xml

        metas = []
        metas.append(comic_series.format(series))
        metas.append(comic_writer.format(writer))

        # add volume information
        if vol != -1:
            metas.append(comic_volume.format(vol))

        # add summary information
        if summary != "":
            metas.append(comic_summary.format(summary))

        # add bookmark information
        if len(table_content) > 0:
            metas.append(comic_pages_op)
            for content in table_content:
                metas.append(comic_page.format(
                    content['page'], content['title']))
            metas.append(comic_pages_cl)

        # Debug print metas
        if METADATA_DEBUG:
            print(Fore.CYAN + f'{"Metas:":<20}' + Style.RESET_ALL)
            pprint(metas, indent=2)

        final = xml_containt.format(content="\n".join(metas))

        f = open(os.path.join(target_folder, file_comic_xml),
                "w+", encoding="utf8")
        f.write(final)
        f.close()
        
        print(END_LOG)
    
    except Exception as e:
        if METADATA_DEBUG:
            log_error("MetadataController", "generate_metadata", e)
        raise Exception(MSG_ERR_CONTROLLER_METADATA.format("generate_metadata"))
        
