import glob
import os
import re

from timeMarkerExtractor import time_marker_extractor


def main():
    file_list = glob.glob(os.path.join(os.path.abspath(os.getcwd()), './Test/in/*.txt'))
    file_list.sort(key=lambda x: int(re.search('(input)([0-9]+)(.txt)', x).group(2)))
    for filename in file_list:
        print(filename)
        with open(filename, 'r', encoding="utf8") as infile:
            s = infile.read()
            print("Original Sentence:")
            print(s)
            time_marker_extractor(s)
            print("=" * 50)


if __name__ == '__main__':
    main()
