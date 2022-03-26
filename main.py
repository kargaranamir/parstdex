import os
import json
import pprint

import settings
from parstdex import MarkerExtractor


def main():
    # read all test inputs in Test folder
    test_path = settings.ROOT_DIR + './tests/data.json'
    f = open(test_path, 'r', encoding='utf8')
    test_data = json.load(f)

    model = MarkerExtractor(DEBUG=False)

    for testcase in test_data:
        input_sentence = testcase['test_input']
        print(f"Original Sentence:\n{input_sentence}")
        # time_marker_extractor will return normalized sentence and time-date markers
        markers = model.extract_marker(input_sentence)

        print("\n")
        # Print extracted markers
        print("All Extracted Markers:")
        print(markers)
        for key in markers.keys():
            print(f"result for {key}:")
            for item in markers[key]:
                print(input_sentence[item[0]:item[1]])

        print("\n")
        markers, values = model.extract_value(input_sentence)
        print("All Extracted Values:")
        print(values)

        print("\n")
        markers, ners = model.extract_ner(input_sentence)
        print("All Extracted NER:")
        print(ners)

        print("==" * 50)


if __name__ == '__main__':
    main()
