import argparse
import os
from icecream import ic
import sys

from common.Commons import extract_number
from controllers.ArchiveController import archive_folder


def main():
    parser = argparse.ArgumentParser(
        description='Archive folders')
    parser.add_argument('-o', type=str, required=True, help='Target folder')
    parser.add_argument('-m', action='store_true', help='Is multiple folders')
    parser.add_argument('-d', default=False, action='store_true', help='Is delete folders after archiving')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

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
