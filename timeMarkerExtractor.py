import re
from pattern_to_regex import Patterns
from utilities.Utilities import Normalizer, deleteSubMatches
from utilities.word_to_value import date_value_extractor

def time_marker_extractor(input_sentence):
    """
    function should output list of strings, each item in list is a time marker present in the input sentence.
    :param input_sentence:
    :return:
    """
    normalizer = Normalizer()
    patterns = Patterns()
    input_sentence = normalizer.normalize_cumulative(input_sentence)
    print("Normalized Sentence:\n", input_sentence)
    output = []
    date_list = []

    # Write Regexes into pattern.txt file
    with open('patterns.txt', 'w', encoding="utf-8") as f:
        f.writelines(patterns.regexes)

    for key in patterns.regexes.keys():
        for regex_value in patterns.regexes[key]:
            out = re.findall(fr'\b(?:{regex_value})', input_sentence)
            output.append(out)

            if key == 'Date' and len(out) > 0:
                for out_dates in out:
                    date_list.append(date_value_extractor(out_dates))

    # process result
    res = [x for x in output if len(x) > 0]
    res = [item for sublist in res for item in sublist]
    res = list(set(res))
    res = deleteSubMatches(res)
    res_date = deleteSubMatches(date_list)

    print("Extracted Markers: ")
    print(res)
    print("Date List: ")
    print(res_date)
    return res