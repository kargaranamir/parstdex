import pytest
import json
import ast
import os
from parstdex import MarkerExtractor


def prepare_test_scenarios():
    file_path = './data.json'

    # Read Test file
    test_data_file = open(file_path, 'r', encoding='utf8')
    test_inputs = json.load(test_data_file)

    # Create test scenarios
    scenarios = []
    for test in test_inputs:
        test_input = test['test_input']
        spans = ast.literal_eval(test['expected'])
        scenarios.append(
            (test_input, spans)
        )

    return scenarios


extractor = MarkerExtractor()
test_scenarios = prepare_test_scenarios()


@pytest.mark.parametrize("sentence, expected", test_scenarios)
def test_parstdex_extractor(sentence, expected):
    extraction_result = extractor.time_marker_extractor(sentence)
    assert extraction_result[2]['Date+Time'] == expected
