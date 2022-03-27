import json
import pprint

import settings
from parstdex import Parstdex


def examples():
    # read all test inputs in Test folder
    test_path = settings.ROOT_DIR + './tests/data.json'
    f = open(test_path, 'r', encoding='utf8')
    test_data = json.load(f)

    model = Parstdex(debug_mode=False)

    result = {}
    for testcase in test_data:
        input_sentence = testcase['test_input']
        result['sentence'] = input_sentence
        # time_marker_extractor will return normalized sentence and time-date markers
        markers = model.extract_marker(input_sentence)
        result['markers'] = markers

        values = model.extract_value(input_sentence)
        result['values'] = values

        ners = model.extract_ner(input_sentence)
        result['ner'] = ners

        pprint.pprint(result)
        print("==" * 50)
