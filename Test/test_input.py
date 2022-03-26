import pytest
import json
import ast
import os
from parstdex import MarkerExtractor


def create_data():
    file_path = os.getcwd() + '/inputs.json'
    f = open(file_path, 'r', encoding='utf8')
    data = json.load(f)

    scenarios = []
    for i in data:
        sentence = i['in']
        spans = i['out']
        scenarios.append((sentence, ast.literal_eval(spans)))

    return scenarios


extractor = MarkerExtractor()
input_data = create_data()


@pytest.mark.parametrize("sentence, span", input_data)
def test_input(sentence, span):
    assert extractor.time_marker_extractor(sentence)[2]['Date+Time'] == span
