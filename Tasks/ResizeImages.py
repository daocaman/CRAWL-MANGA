import argparse
from icecream import ic
import os

import sys

# add the path to the common folder
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\common')))
from Commons import resize_image, extract_number

def main():
    parser = argparse.ArgumentParser(
        description='Archive folders')
    parser.add_argument('-o', type=str, required=True, help='target folder')
    parser.add_argument('-m', action='store_true', help='multiple folders')
    parser.add_argument('-hr', default=False, action='store_true', help='Resize to horizontal')

    args = parser.parse_args()

    if args.m:
        folders = os.listdir()
        folders = [f for f in folders if os.path.isdir(f) and args.o in f]
        folders = sorted(folders, key=lambda x: extract_number(x, True))
        for fol in folders:
            resize_image(fol, args.hr)
    else:
        resize_image(args.o, args.hr)

if __name__ == "__main__":
    main()
