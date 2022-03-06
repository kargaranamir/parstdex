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
            # time_marker_extractor will return normalized sentence and time-date markers
            normalized_sentence, output_raw, result = extractor.time_marker_extractor(input_sentence)

            # Print results
            print("Normalized Sentence:\n", normalized_sentence)

            print("Time Raw Output:\n", output_raw.get('Time', []))
            print("Date Raw Output:\n", output_raw.get('Date', []))
            print("All Extracted Markers: ")
            print(result)
            for item in result:
                print(normalized_sentence[item[0]:item[1]])

            # time_value_extractor will return normalized sentence and time-date markers and values
            # normalized_sentence, result, values = extractor.time_value_extractor(input_sentence)

            # Print results
            # print("Normalized Sentence:\n", normalized_sentence)
            # print("All Extracted Markers: ")
            # print(result)
            # for item in result:
            #     print(normalized_sentence[item[0]:item[1]])

            # print("All Value Markers Extracted: ")
            # print(values)


if __name__ == '__main__':
    main()
