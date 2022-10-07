import os
import shutil
from icecream import ic

for fol in os.listdir():
    if os.path.isdir(fol) and "vol" in fol.lower():
        ic("Archive " + fol + ".zip")
        shutil.make_archive(fol, "zip", base_dir=fol)
