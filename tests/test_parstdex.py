import pytest
import json
import ast
import os
from parstdex import MarkerExtractor
from settings import ROOT_DIR


def prepare_test_scenarios():
    file_path = ROOT_DIR + '/tests/data.json'

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


model = MarkerExtractor()
test_scenarios = prepare_test_scenarios()


@pytest.mark.parametrize("sentence, expected", test_scenarios)
def test_parstdex_extractor(sentence, expected):
    markers = model.extract_marker(sentence)
    assert markers['Date+Time'] == expected
