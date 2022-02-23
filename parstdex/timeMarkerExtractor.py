import re
from parstdex.utils.pattern_to_regex import Patterns
from parstdex.utils.normalizer import Normalizer
from parstdex.utils.word_to_value import ValueExtractor
from parstdex.utils.merge_spans import merge_spans

class MarkerExtractor:
    def __init__(self, normalizer=None, patterns=None, value_extractor=None):
        # Normalizer: manage spaces, converts numbers to en, converts alphabet to fa
        self.normalizer = normalizer if normalizer else Normalizer()
        # Patterns: patterns to regex generator
        self.patterns = patterns if patterns else Patterns()
        # ValueExtractor: value extractor from known time and date
        self.value_extractor = value_extractor if value_extractor else ValueExtractor()

    def time_marker_extractor(self, input_sentence, ud_patterns=None):
        """
        function should output list of spans, each item in list is a time marker span present in the input sentence.
        :param input_sentence: input sentence
        :return:
        normalized_sentence: normalized sentence
        result: all extracted spans
        """

        # Normalizer: manage spaces, converts numbers to en, converts alphabet to fa
        normalizer = self.normalizer
        # Patterns: patterns to regex generator
        patterns = ud_patterns if ud_patterns else self.patterns

        # apply normalizer on input sentence
        normalized_sentence = normalizer.normalize_cumulative(input_sentence)

        # define data structures to compute and postprocess the extracted patterns
        output_raw = {"Date": [], "Time": []}
        output_extracted = {}

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
                    matches = list(re.finditer(fr'\b(?:{regex_value})', normalized_sentence))
                    # store extracted markers in output_raw
                    output_raw[key] = output_raw[key] + matches


        spans = []
        spans_key = []
        for key in output_raw.keys():
            matches = output_raw[key]
            for match in matches:
                start = match.regs[0][0]
                end = match.regs[0][1]
                # match.group()
                spans.append((start, end))
                spans_key.append(key)

        if len(spans) == 0:
            return normalized_sentence, []

        result = merge_spans(spans, spans_key)
        return normalized_sentence, result

    def time_value_extractor(self, input_sentence):
        """
        function should output list of values, each item in list is a time marker value present in the input sentence.
        :param input_sentence: input sentence
        :return:
        normalized_sentence: normalized sentence
        result: all extracted spans
        values: all extracted time-date values

        """

        normalized_sentence, result = self.time_marker_extractor(input_sentence)
        output_extracted = [normalized_sentence[item[0]:item[1]] for item in result]
        values = [self.value_extractor.compute_value(p) for p in output_extracted]

        return normalized_sentence, result, values
