import argparse
import os

import sys

# add the path to the common folder
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\common')))
from Commons import reformat_folder, extract_number

def main():
    parser = argparse.ArgumentParser(
        description='Reformat old folder')
    parser.add_argument('-o', type=str, required=True, help='Target folder')
    parser.add_argument('-m', default=False, action='store_true', help='Is multiple folders')
    parser.add_argument('-d', default=False, action='store_true', help='Is delete child folders after reformat')

    args = parser.parse_args()

    if args.m:
        folders = os.listdir()
        folders = [f for f in folders if os.path.isdir(f) and args.o in f]
        folders = sorted(folders, key=lambda x: extract_number(x, True))

        for fol in folders:
            reformat_folder(fol, args.d)
    else:
        reformat_folder(args.o, args.d)

if __name__ == "__main__":
    main()