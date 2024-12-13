import argparse
import os

import sys

# add the path to the common folder
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\common')))
from Commons import extract_number, generate_filename, is_image_file
from Constants import file_prefix

def main():
    parser = argparse.ArgumentParser(
        description='Rename files')
    parser.add_argument('-o', type=str, required=True, help='target folder')
    parser.add_argument('-s', type=int, default=0, help='Sort file')
    parser.add_argument('-s_i', type=int, default=0, help='Start index')

    args = parser.parse_args()

    files = os.listdir(args.o)
    files = [f for f in files if is_image_file(f)]

    if args.s == 1:
        files = sorted(files, key=lambda x: extract_number(x))
    
    if args.s == 2:
        files = sorted(files, key=lambda x: extract_number(x, True))

    for i, f in enumerate(files):
        new_name = generate_filename(file_prefix, args.s_i + i, ".jpg")
        os.rename(os.path.join(args.o, f), os.path.join(args.o, new_name))
        
if __name__ == "__main__":
    main()