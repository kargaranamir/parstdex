import os
import json

from parstdex import MarkerExtractor


def main():
    # read all test inputs in Test folder
    test_path = os.getcwd() + './Test/inputs.json'
    f = open(test_path, 'r', encoding='utf8')
    test_data = json.load(f)
    extractor = MarkerExtractor()

    for testcase in test_data:
        input_sentence = testcase['in']
        print("Original Sentence:\n", input_sentence)
        # time_marker_extractor will return normalized sentence and time-date markers
        normalized_sentence, output_raw, result = extractor.time_marker_extractor(input_sentence)

        # Print results
        print("Normalized Sentence:\n", normalized_sentence)

        # Print extracted markers
        print("All Extracted Markers: ")
        print(result)
        for item in result:
            print(normalized_sentence[item[0]:item[1]])

        ## time_value_extractor will return normalized sentence and time-date markers and values
        # normalized_sentence, result, values = extractor.time_value_extractor(input_sentence)
        #
        ## Print results
        # print("Normalized Sentence:\n", normalized_sentence)
        # print("All Extracted Markers: ")
        # print(result)
        # for item in result:
        #     print(normalized_sentence[item[0]:item[1]])
        #
        # print("All Value Markers Extracted: ")
        # print(values)


if __name__ == '__main__':
    main()
