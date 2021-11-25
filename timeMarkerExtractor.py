import re
from pattern_to_regex import Patterns
from utilities.Utilities import Normalizer, deleteSubMatches


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

    # Write Regexes into pattern.txt file
    with open('patterns.txt', 'w', encoding="utf-8") as f:
        f.writelines(patterns.regexes)

    for i in range(len(patterns.regexes)):
        out = re.findall(fr'\b(?:{patterns.regexes[i]})', input_sentence)
        output.append(out)

    # process result
    res = [x for x in output if len(x) > 0]
    res = [item for sublist in res for item in sublist]
    res = list(set(res))
    res = deleteSubMatches(res)

    print("Extracted Markers:")
    print(res)

    return res