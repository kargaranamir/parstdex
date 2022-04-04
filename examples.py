import json
import pprint

from parstdex import Parstdex, settings


def examples():
    # read all test inputs in Test folder
    test_path = settings.ROOT_DIR + '/tests/data.json'
    f = open(test_path, 'r', encoding='utf-8-sig')
    test_data = json.load(f)

    model = Parstdex(debug_mode=True)

    result = {}
    for testcase in test_data:
        input_sentence = testcase['test_input']
        result['sentence'] = input_sentence
        # time_marker_extractor will return normalized sentence and time-date markers

        spans = model.extract_span(input_sentence)
        result['spans'] = spans

        markers = model.extract_marker(input_sentence)
        result['markers'] = markers

        values = model.extract_value(input_sentence)
        result['values'] = values

        ners = model.extract_ner(input_sentence)
        result['ner'] = ners

        pprint.pprint(result,)
        print("==" * 50)


examples()
