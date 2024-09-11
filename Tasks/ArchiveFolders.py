import argparse
import os
from icecream import ic

import sys

# add the path to the common folder
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\common')))
from Commons import archive_folder, extract_number

def main():
    parser = argparse.ArgumentParser(
        description='Archive folders')
    parser.add_argument('-o', type=str, required=True, help='target folder')
    parser.add_argument('-m', action='store_true', help='multiple folders')
    parser.add_argument('-d', default=False, action='store_true', help='delete folders after archiving')

    args = parser.parse_args()

    if args.m:
        ic(args.m)
        folders = os.listdir()
        folders = [f for f in folders if os.path.isdir(f) and args.o in f]
        folders = sorted(folders, key=lambda x: extract_number(x, True))
        for fol in folders:
            archive_folder(fol, args.d)
    else:
        archive_folder(args.o, args.d)

if __name__ == "__main__":
    main()
