import re
from pattern_to_regex import Patterns
from utilities.Utilities import Normalizer, deleteSubMatches
from utilities.word_to_value import ValueExtractor


def time_marker_extractor(input_sentence):
    """
    function should output list of strings, each item in list is a time marker present in the input sentence.
    :param input_sentence: input sentence
    :return:
    normalized_sentence: normalized sentence
    res: all extracted markers
    res_date: all extracted date values
    res_time: all extracted time values
    """

    # Normalizer: manage spaces, converts numbers to en, converts alphabet to fa
    normalizer = Normalizer()
    # Patterns: patterns to regex generator
    patterns = Patterns()
    # ValueExtractor: value extractor from known time and date
    extractor = ValueExtractor()

    # apply normalizer on input sentence
    normalized_sentence = normalizer.normalize_cumulative(input_sentence)

    # define data structures to compute and postprocess the extracted patterns
    output_raw = {"Date": [], "Time": []}
    output_extracted = {}
    output_flatten: list = []
    output_flatten_keys = []
    post_output_flatten = []
    post_output_flatten_keys = []

    # data structures to store all extracted markers data-time values
    res = []
    res_date = []
    res_time = []

    # write Regexes into pattern.txt file
    with open('patterns.txt', 'w', encoding="utf-8") as f:
        for key in patterns.regexes.keys():
            for regex_value in patterns.regexes[key]:
                f.write(regex_value)
                f.write('\n')

    # add pattern keys to dictionaries and define a list structure for each key
    for key in patterns.regexes.keys():
        output_raw[key]: list = []
        output_extracted[key]: list = []

    # apply regexes on normalized sentence and store extracted markers in output_raw
    for key in patterns.regexes.keys():
        for regex_value in patterns.regexes[key]:
            # apply regex
            out = re.findall(fr'\b(?:{regex_value})', normalized_sentence)
            # ignore empty markers
            if len(out) > 0:
                # store extracted markers in output_raw
                output_raw[key] = output_raw[key] + out

    # process result: make flatten value-key lists from dictionary
    for key in output_raw.keys():
        output_raw[key] = list(set(output_raw[key]))
        output_flatten = output_flatten + output_raw[key]
        output_flatten_keys = output_flatten_keys + [key] * len(output_raw[key])

    # make values unique while they have different keys
    for key, value in zip(output_flatten_keys, output_flatten):
        if not value in post_output_flatten:
            post_output_flatten.append(value)
            post_output_flatten_keys.append(key)

    # store unique values in output_flatten and corresponding keys in output_flatten_keys
    output_flatten = post_output_flatten
    output_flatten_keys = post_output_flatten_keys

    # delete extracted markers the cover each other and get the longest one
    output_extracted = deleteSubMatches(output_flatten, output_flatten_keys, normalized_sentence)
    # extract date values from all post process markers
    if output_extracted.get('Date'):
        res_date = [extractor.compute_date_value(p_date) for p_date in output_extracted['Date']]
    # extract time values from all post process markers
    if output_extracted.get('Time'):
        res_time = [extractor.compute_time_value(p_time) for p_time in output_extracted['Time']]
    # make all the extracted markers flatten into a one list
    for p_output in output_extracted.values():
        res += p_output

    return normalized_sentence, res, res_date, res_time