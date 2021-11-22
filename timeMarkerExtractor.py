import re
from pattern_to_regex import res_pattern_list as pattern_list


def time_marker_extractor(input_sentence):
    """
    function should output list of strings, each item in list is a time marker present in the input sentence.
    :param input_sentence:
    :return:
    """

    output = []
    for i in range(len(pattern_list)):
        out = re.findall(fr'\b(?:{pattern_list[i]})', input_sentence)
        output.append(out)

    res = max(output, key=len)

    return [res]