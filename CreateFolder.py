import os
import shutil
import re

prefix = "Weathering with you"

vol_length = 3

for i in range(1, vol_length+1):
    os.mkdir(prefix + ' - Vol'+str(i))

