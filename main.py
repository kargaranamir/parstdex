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
            input_sentence = infile.read()
            print("Original Sentence:\n", input_sentence)
            normalized_sentence, res, res_date, res_time = time_marker_extractor(input_sentence)
            print("Normalized Sentence:\n", normalized_sentence)
            print("=" * 50)
            print("All Extracted Markers: ")
            print(res)
            print("Date Value List: ")
            print(res_date)
            print("Time Value List: ")
            print(res_time)

if __name__ == '__main__':
    main()
