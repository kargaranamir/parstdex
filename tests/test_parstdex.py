import pytest
import json
import ast

from parstdex import Parstdex, settings


def prepare_test_scenarios():
    file_path = settings.ROOT_DIR + '/tests/data.json'

    # Read Test file
    test_data_file = open(file_path, 'r', encoding='utf-8-sig')
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


model = Parstdex()
test_scenarios = prepare_test_scenarios()


@pytest.mark.parametrize("sentence, expected", test_scenarios)
def test_parstdex_extractor(sentence, expected):
    spans = model.extract_span(sentence)
    assert json.loads(spans)['datetime'] == expected
