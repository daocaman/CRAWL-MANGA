import os
import shutil

tmpPath = ""
for fol in os.listdir():
    print(fol)
    if os.path.isdir(fol):
        tmpPath = fol
        for tinyFol in os.listdir(fol):
            print("tiny folder: ", tinyFol)
            if os.path.isdir(fol+"/"+tinyFol) and ("_files" in tinyFol):
                shutil.rmtree(fol+"/"+tinyFol)
                if os.path.exists(fol+"/"+tinyFol.split("_files")[0]+".html"):
                    os.remove(fol+"/"+tinyFol.split("_files")[0]+".html")