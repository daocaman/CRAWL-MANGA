import argparse
import os

import sys

# add the path to the common folder
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\common')))
from Commons import get_info_chapter

def main():
    parser = argparse.ArgumentParser(
        description='Getting chapter information')
    parser.add_argument('-l', type=str, required=True, help='Link web')
    parser.add_argument('-x_p', type=str, required=True, help='Target element')
    parser.add_argument('-m', default=False, action='store_true', help='Is multiple chapters')
    parser.add_argument('-c_e', type=str, default="", help='Child elements')

    args = parser.parse_args()

    if args.m:
        get_info_chapter(args.l, args.x_p, True, args.c_e)
    else:
        get_info_chapter(args.l, args.x_p, False, args.c_e)
if __name__ == "__main__":
    main()