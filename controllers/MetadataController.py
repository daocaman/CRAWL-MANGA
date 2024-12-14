import os
from colorama import Fore, Style
from pprint import pprint

from common.Constants import METADATA_DEBUG, file_comic_xml, comic_xml, comic_series, comic_writer, comic_volume, comic_summary, comic_page, comic_pages_op, comic_pages_cl

def generate_metadata(series, writer, vol=-1, table_content=[], summary="", target_folder=""):
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
        print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'MetadataController: generate_metadata'.center(70) + Style.RESET_ALL)
        print(Fore.GREEN + f'{"Generate metadata":<20}' + Style.RESET_ALL + f'{str(series): >49}')
        print(Fore.BLUE + f'{"Series:":<20}' + Style.RESET_ALL + f'{str(series): >49}')
        print(Fore.BLUE + f'{"Writer:":<20}' + Style.RESET_ALL + f'{str(writer): >49}')
        print(Fore.BLUE + f'{"Vol:":<20}' + Style.RESET_ALL + f'{str(vol): >49}')
        print(Fore.BLUE + f'{"Summary:":<20}' + Style.RESET_ALL + f'{str(summary): >49}')
        print(Fore.BLUE + f'{"Target folder:":<20}' + Style.RESET_ALL + f'{str(target_folder): >49}')
        print(Fore.BLUE + f'{"Table content:":<20}' + Style.RESET_ALL )
        pprint(table_content, indent=2)
    
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
    
    # Debug print final
    METADATA_DEBUG and print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
