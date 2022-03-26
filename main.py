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
    extractor = MarkerExtractor()

    for testcase in test_data:
        input_sentence = testcase['test_input']
        print(f"Original Sentence:\n{input_sentence}")
        # time_marker_extractor will return normalized sentence and time-date markers
        normalized_sentence, output_raw, result = extractor.time_marker_extractor(input_sentence)

        # Print results
        print(f"Normalized Sentence:\n{normalized_sentence}")

        # Print raw output
        dict_output_raw = {}
        for key in output_raw.keys():
            dict_output_raw[key] = []
            for match in output_raw[key]:
                start = match.regs[0][0]
                end = match.regs[0][1]
                dict_output_raw[key].append({
                    "token": match.string[start:end],
                    "span": [start, end]
                })

        PRINT_RAW = False
        if PRINT_RAW:
            print("Raw Output:")
            pprint.pprint(dict_output_raw)

        # Print extracted markers
        print("All Extracted Markers: ")
        print(result)
        for key in result.keys():
            print(f"result for {key}:")
            for item in result[key]:
                print(normalized_sentence[item[0]:item[1]])

        print("==" * 50)


if __name__ == '__main__':
    main()
