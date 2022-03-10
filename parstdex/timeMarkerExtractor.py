import re
from parstdex.utils.pattern_to_regex import Patterns
from parstdex.utils.normalizer import Normalizer
from parstdex.utils.spans import create_spans, subtract_spans
from parstdex.utils.word_to_value import ValueExtractor
from parstdex.utils.spans import merge_spans


class MarkerExtractor:
    def __init__(self, normalizer=None, patterns=None, adv_patterns=None, value_extractor=None):
        # Normalizer: manage spaces, converts numbers to en, converts alphabet to fa
        self.normalizer = normalizer if normalizer else Normalizer()
        # Patterns: patterns to regex generator
        self.patterns = patterns if patterns else Patterns('pattern/positive')
        # Adversarial Patterns: patterns to regex generator
        self.adv_patterns = adv_patterns if adv_patterns else Patterns('pattern/negative')
        # ValueExtractor: value extractor from known time and date
        self.value_extractor = value_extractor if value_extractor else ValueExtractor()

    def time_marker_extractor(self, input_sentence):
        """
        function should output list of spans, each item in list is a time marker span present in the input sentence.
        :param ud_patterns:
        :param input_sentence: input sentence
        :return:
        normalized_sentence: normalized sentence
        result: all extracted spans
        """

        # Normalizer: manage spaces, converts numbers to en, converts alphabet to fa
        normalizer = self.normalizer
        # Patterns: patterns to regex generator
        patterns = self.patterns
        # Adversarial patterns
        adv_patterns = self.adv_patterns

        # apply normalizer on input sentence
        normalized_sentence = normalizer.normalize_cumulative(input_sentence)

        # Create normal spans
        output_raw, spans, spans_key = create_spans(normalized_sentence, patterns)

        if len(spans) == 0:
            return normalized_sentence, output_raw, []

        # e.x. [(0, 15), (26, 35), (37, 42)]
        normal_spans = merge_spans(spans, spans_key)

        # Create Adversarial spans
        adv_output_raw, adv_spans, adv_spans_key = create_spans(normalized_sentence, adv_patterns)

        # e.x. [(3, 10)]
        adv_spans = merge_spans(adv_spans, adv_spans_key)

        # Subtract Adversarial spans from normal spans
        result = subtract_spans(normal_spans, adv_spans)

        return normalized_sentence, output_raw, result

    def time_value_extractor(self, input_sentence):
        """
        function should output list of values, each item in list is a time marker value present in the input sentence.
        :param input_sentence: input sentence
        :return:
        normalized_sentence: normalized sentence
        result: all extracted spans
        values: all extracted time-date values
        """

        normalized_sentence, output_raw, result = self.time_marker_extractor(input_sentence)
        output_extracted = [normalized_sentence[item[0]:item[1]] for item in result]
        values = [self.value_extractor.compute_value(p) for p in output_extracted]

        return normalized_sentence, result, values