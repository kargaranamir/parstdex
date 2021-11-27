import re
from pattern_to_regex import Patterns
from utilities.Utilities import Normalizer, deleteSubMatches
from utilities.word_to_value import ValueExtractor


def time_marker_extractor(input_sentence):
    """
    function should output list of strings, each item in list is a time marker present in the input sentence.
    :param input_sentence:
    :return:
    """
    normalizer = Normalizer()
    patterns = Patterns()
    extractor = ValueExtractor()

    input_sentence = normalizer.normalize_cumulative(input_sentence)
    print("Normalized Sentence:\n", input_sentence)
    output_raw = {}
    output_extracted = {}
    output_flatten : list = []
    output_flatten_keys = []
    res = []
    res_date = []
    # Write Regexes into pattern.txt file
    with open('patterns.txt', 'w', encoding="utf-8") as f:
        f.writelines(patterns.regexes)

    for key in patterns.regexes.keys():
        output_raw [key] : list = []
        output_extracted [key] : list = []

    for key in patterns.regexes.keys():
        for regex_value in patterns.regexes[key]:
            out = re.findall(fr'\b(?:{regex_value})', input_sentence)
            if len(out) > 0:
                output_raw[key] = output_raw[key] + out
            #
            # if key == 'Date' and len(out) > 0:
            #     for out_dates in out:
            #         date_list.append(extractor.compute_date_value(out_dates))

    # process result
    for key in output_raw.keys():
        output_raw[key] = list(set(output_raw[key]))
        output_flatten = output_flatten + output_raw [key]
        output_flatten_keys = output_flatten_keys + [key] * len(output_raw[key])


    output_extracted = deleteSubMatches(output_flatten, output_flatten_keys, input_sentence)
    if output_extracted.get('Date'):
        res_date = [extractor.compute_date_value(p_date) for p_date in output_extracted['Date'] ]
    for p_output in output_extracted.values():
        res.append(p_output)

    print("Extracted Markers: ")
    print(res)
    print("Date List: ")
    print(res_date)
    return res