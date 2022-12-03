import os
import shutil

for fol in os.listdir():
    if os.path.isdir(fol) and "Vol" in fol:
        for miniFol in os.listdir(fol):
            if os.path.isdir(fol+"/"+miniFol) and miniFol != "00_Cover":
                shutil.move(fol+"/"+miniFol,miniFol, copy_function=shutil.copytree)

