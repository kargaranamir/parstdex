import pprint

import nltk
import textspan

from parstdex.utils.normalizer import Normalizer
from parstdex.utils.pattern_to_regex import Patterns
from parstdex.utils.spans import create_spans
from parstdex.utils.spans import merge_spans
from parstdex.utils.word_to_value import ValueExtractor


class MarkerExtractor:
    def __init__(self, DEBUG=False):
        # Normalizer: convert arabic YE and KAF to persian ones.
        self.normalizer = Normalizer()
        # Patterns: patterns to regex generator
        self.patterns = Patterns()
        # ValueExtractor: value extractor from known time and date
        self.value_extractor = ValueExtractor()
        self.DEBUG = DEBUG

    def extract_marker(self, input_sentence: str):
        """
        function should output list of spans, each item in list is a time marker span present in the input sentence.
        :param input_sentence: input sentence
        :return:
        markers: all extracted spans
        """

        # apply normalizer on input sentence
        normalized_sentence = self.normalizer.normalize_cumulative(input_sentence)

        # Create spans
        output_raw, spans = create_spans(self.patterns, normalized_sentence)

        if self.DEBUG:
            # Print raw output
            dict_output_raw = {}
            for key in output_raw.keys():
                dict_output_raw[key] = []
                for match in output_raw[key]:
                    start = match.regs[0][0]
                    end = match.regs[0][1]
                    dict_output_raw[key].append({
                        "token": match.string[start:end],
                        "span": [start, end]
                    })
            pprint.pprint(dict_output_raw)

        if len(spans['Time']) == 0 and len(spans['Date']) == 0:
            return {'Date+Time':[], 'Date':[], 'Time':[]}

        markers = merge_spans(spans, normalized_sentence)

        return markers

    def extract_value(self, input_sentence: str):
        """
        function should output list of values, each item in list is a time marker value present in the input sentence.
        :param input_sentence: input sentence
        :return:
        normalized_sentence: normalized sentence
        result: all extracted spans
        values: all extracted time-date values
        """

        markers = self.extract_marker(input_sentence)
        spans = markers['Date+Time']
        output_extracted = [input_sentence[item[0]:item[1]] for item in spans]
        values = [self.value_extractor.compute_value(p) for p in output_extracted]

        return markers, values

    def extract_ner(self, input_sentence: str):

        markers = self.extract_marker(input_sentence)
        spans = markers['Date+Time']
        ners = []
        tokens = nltk.word_tokenize(input_sentence)
        all_spans = textspan.get_original_spans(tokens, input_sentence)
        all_spans = [span[0] for span in all_spans if span != []]
        for span in all_spans:
            chosen = False
            for ner_span in spans:
                if span[0] >= ner_span[0] and span[1] <= ner_span[1]:
                    if span[0] == ner_span[0]:
                        ners.append((input_sentence[span[0]:span[1]], 'B-DAT'))
                    else:
                        ners.append((input_sentence[span[0]:span[1]], 'I-DAT'))
                    chosen = True
                    break
            if not chosen:
                ners.append((input_sentence[span[0]:span[1]], 'O'))
        return markers, ners