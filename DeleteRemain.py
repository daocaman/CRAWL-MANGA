import os
import shutil
from icecream import ic

tmpPath = ""
for fol in os.listdir():
    ic(fol)
    if os.path.isdir(fol):
        tmpPath = fol
        for tinyFol in os.listdir(fol):
            ic("tiny folder: ", tinyFol)
            if os.path.isdir(fol+"/"+tinyFol) and ("_files" in tinyFol):
                shutil.rmtree(fol+"/"+tinyFol)
                if os.path.exists(fol+"/"+tinyFol.split("_files")[0]+".html"):
                    os.remove(fol+"/"+tinyFol.split("_files")[0]+".html")