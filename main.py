import glob
import os
import re

from parstdex import MarkerExtractor

def main():
    # read all test inputs in Test folder
    file_list = glob.glob(os.path.join(os.path.abspath(os.getcwd()), './Test/in/*.txt'))
    file_list.sort(key=lambda x: int(re.search('(input)([0-9]+)(.txt)', x).group(2)))
    extractor = MarkerExtractor()
    for filename in file_list:
        print(filename)
        with open(filename, 'r', encoding="utf8") as infile:
            # read input test file
            input_sentence = infile.read()
            print("Original Sentence:\n", input_sentence)
            # time_marker_extractor will return normalized sentence and time and date markers and corresponding
            # value evaluation
            normalized_sentence, res, res_date, res_time = extractor.time_marker_extractor(input_sentence)

            # Print results
            print("Normalized Sentence:\n", normalized_sentence)
            print("All Extracted Markers: ")
            print(res)
            print("Date Value List: ")
            print(res_date)
            print("Time Value List: ")
            print(res_time)
            print("=" * 50)


if __name__ == '__main__':
    main()
