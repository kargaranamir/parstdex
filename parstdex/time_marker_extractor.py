import nltk
import textspan

from parstdex.utils.normalizer import Normalizer
from parstdex.utils.pattern_to_regex import Patterns
from parstdex.utils.spans import create_spans
from parstdex.utils.spans import merge_spans
from parstdex.utils.word_to_value import ValueExtractor


class MarkerExtractor:
    def __init__(self, normalizer=None, patterns=None, adv_patterns=None, value_extractor=None):
        # Normalizer: convert arabic YE and KAF to persian ones.
        self.normalizer = normalizer if normalizer else Normalizer()
        # Patterns: patterns to regex generator
        self.patterns = patterns if patterns else Patterns()
        # ValueExtractor: value extractor from known time and date
        self.value_extractor = value_extractor if value_extractor else ValueExtractor()

    def time_marker_extractor(self, input_sentence: str):
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
        patterns = self.patterns

        # apply normalizer on input sentence
        normalized_sentence = normalizer.normalize_cumulative(input_sentence)

        # Create spans
        output_raw, spans = create_spans(patterns, normalized_sentence)

        if len(spans['Time']) == 0 and len(spans['Date']) == 0:
            return normalized_sentence, output_raw, {}

        result = merge_spans(spans, normalized_sentence)

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
        spans = result['Date+Time']
        output_extracted = [normalized_sentence[item[0]:item[1]] for item in spans]
        values = [self.value_extractor.compute_value(p) for p in output_extracted]

        return normalized_sentence, result, values

    def time_ner_extractor(self, input_sentence: str):

        sentence, output_raw, spans = self.time_marker_extractor(input_sentence)
        spans = spans['Date+Time']
        result = []
        tokens = nltk.word_tokenize(sentence)
        all_spans = textspan.get_original_spans(tokens, sentence)
        all_spans = [span[0] for span in all_spans if span != []]
        for span in all_spans:
            chosen = False
            for ner_span in spans:
                if span[0] >= ner_span[0] and span[1] <= ner_span[1]:
                    if span[0] == ner_span[0]:
                        result.append((sentence[span[0]:span[1]], 'B-DAT'))
                    else:
                        result.append((sentence[span[0]:span[1]], 'I-DAT'))
                    chosen = True
                    break
            if not chosen:
                result.append((sentence[span[0]:span[1]], 'O'))
        return result
