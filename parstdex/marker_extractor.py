import pprint
import re

from parstdex.utils import const
from parstdex.utils.tokenizer import tokenize_words
import textspan

from parstdex.utils.normalizer import Normalizer
from parstdex.utils.pattern_to_regex import Patterns
from parstdex.utils.spans import create_spans, merge_spans, filter_span_in_range
from parstdex.utils.deprecation import deprecated

re._MAXCACHE = 512


class MarkerExtractor(object):
    def __init__(self, debug_mode=False):
        # Normalizer: convert arabic YE and KAF to persian ones.
        self.normalizer = Normalizer()
        # Patterns: patterns to regex generator
        patterns = Patterns.getInstance()
        regex_patterns = patterns.regexes
        self.regexes = {}
        for key, regex_to_compile in regex_patterns.items():
            self.regexes[key] = []
            for regex in regex_to_compile:
                self.regexes[key].append(
                    re.compile(fr'(?:\b|(?!{const.FA_SYM}|\d+))(?:{regex})(?:\b|(?!{const.FA_SYM}|\d+))', 0))

        self.DEBUG = debug_mode
        self.extract_span("")
        annotations = patterns.cumulative_annotations
        self.duration_annotations = annotations["CJ"] + "|" + annotations["TOOL"]
        self.set_annotations = annotations["HAR"]
        super(MarkerExtractor, self).__init__()

    def extract_span(self, input_sentence: str):
        """
        function should output list of spans, each item in list is a time marker span present in the input sentence.
        :param input_sentence: input sentence
        :return:
        markers: all extracted spans
        """

        # apply normalizer on input sentence
        normalized_sentence = self.normalizer.normalize_cumulative(input_sentence)

        # Create spans
        output_raw, spans = create_spans(self.regexes, normalized_sentence)

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

        if len(spans['time']) == 0 and len(spans['date']) == 0:
            return {'datetime': [], 'date': [], 'time': []}

        spans = merge_spans(spans, normalized_sentence)

        return spans

    def extract_marker(self, input_sentence: str):
        markers = {'datetime': {}, 'date': {}, 'time': {}}

        spans = self.extract_span(input_sentence)
        for key in spans.keys():
            spans_list = spans[key]
            markers[key] = {str(span): input_sentence[span[0]: span[1]] for span in spans_list}

        return markers

    @deprecated("extract_ner will be deprecated soon. Use extract_bio_dat or extract_bio_dattim instead.")
    def extract_ner(self, input_sentence: str, tokenizer=None):
        return self.extract_bio_dat(input_sentence, tokenizer)

    def extract_bio_dat(self, input_sentence: str, tokenizer=None):
        """
        You can pass any custom tokenizer to tokenize sentences.
        :param input_sentence:
        :param tokenizer:
        :return:
        """
        spans_dict = self.extract_span(input_sentence)
        spans = spans_dict['datetime']
        ners = []
        tokens = tokenize_words(input_sentence) if not tokenizer else tokenizer
        all_spans = textspan.get_original_spans(tokens, input_sentence)
        all_spans = [span[0] for span in all_spans if span != []]
        for span in all_spans:
            chosen = False
            for ner_span in spans:
                if ner_span[0] <= span[0] <= ner_span[1]:
                    if span[0] == ner_span[0]:
                        ners.append((input_sentence[span[0]:span[1]], 'B-DAT'))
                    else:
                        ners.append((input_sentence[span[0]:span[1]], 'I-DAT'))
                    chosen = True
                    break
            if not chosen:
                ners.append((input_sentence[span[0]:span[1]], 'O'))
        return ners

    def extract_bio_dattim(self, input_sentence: str, tokenizer=None):
        """
        You can pass any custom tokenizer to tokenize sentences.
        :param input_sentence:
        :param tokenizer:
        :return:
        """
        spans_dict = self.extract_span(input_sentence)
        time_spans = spans_dict['time']
        date_spans = spans_dict['date']
        spans = time_spans + date_spans
        ners = []
        tokens = tokenize_words(input_sentence) if not tokenizer else tokenizer
        all_spans = textspan.get_original_spans(tokens, input_sentence)
        all_spans = [span[0] for span in all_spans if span != []]
        for span in all_spans:
            chosen = False
            for ner_span in spans:
                if ner_span[0] <= span[0] <= ner_span[1]:
                    if span[0] == ner_span[0]:
                        if ner_span in time_spans:
                            ners.append((input_sentence[span[0]:span[1]], 'B-TIM'))
                        elif ner_span in date_spans:
                            ners.append((input_sentence[span[0]:span[1]], 'B-DAT'))
                    else:
                        if ner_span in time_spans:
                            ners.append((input_sentence[span[0]:span[1]], 'I-TIM'))
                        elif ner_span in date_spans:
                            ners.append((input_sentence[span[0]:span[1]], 'I-DAT'))
                    chosen = True
                    break
            if not chosen:
                ners.append((input_sentence[span[0]:span[1]], 'O'))
        return ners

    def extract_time_ml(self, input_sentence: str):
        spans = self.extract_span(input_sentence)

        if len(spans["datetime"]) == 0:
            return input_sentence
        elif len(spans["time"]) == 0:
            working_spans = spans["date"]
        elif len(spans["date"]) == 0:
            working_spans = spans["time"]
        else:
            working_spans = spans["datetime"]

        last_span_index = 0
        output_time_ml = ""
        for span in working_spans:
            output_time_ml = output_time_ml + f"{input_sentence[last_span_index:span[0]]}"
            span_value = input_sentence[span[0]:span[1]]
            last_span_index = span[1]
            if re.search(fr"(?:\b|(?!{const.FA_SYM}|\d+))({self.set_annotations})(?:\b|(?!{const.FA_SYM}|\d+))", span_value):
                output_time_ml = output_time_ml + f"<TIMEX3 type='SET'>{span_value}</TIMEX3>"
            elif re.search(fr"(?:\b|(?!{const.FA_SYM}|\d+))({self.duration_annotations})(?:\b|(?!{const.FA_SYM}|\d+))", span_value):
                output_time_ml = output_time_ml + f"<TIMEX3 type='DURATION'>{span_value}</TIMEX3>"
            elif span in spans["time"]:
                output_time_ml = output_time_ml + f"<TIMEX3 type='TIME'>{span_value}</TIMEX3>"
            elif span in spans["date"]:
                output_time_ml = output_time_ml + f"<TIMEX3 type='DATE'>{span_value}</TIMEX3>"
            else:
                start, end = span
                constituent_spans = filter_span_in_range(start, end, spans["date"] + spans["time"])
                for c_span in constituent_spans:
                    c_span_value = input_sentence[c_span[0]:c_span[1]]
                    if c_span in spans["time"]:
                        output_time_ml = output_time_ml + f"<TIMEX3 type='TIME'>{c_span_value}</TIMEX3>"
                    else:
                        output_time_ml = output_time_ml + f"<TIMEX3 type='DATE'>{c_span_value}</TIMEX3>"

        output_time_ml = output_time_ml + f" {input_sentence[last_span_index:]}"

        return output_time_ml
