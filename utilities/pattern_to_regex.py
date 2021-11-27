import re
import os
from utilities.Utilities import Normalizer
import utilities.const as const


class Annotation:
    annotation_path = 'utilities/annotation'
    normalizer = Normalizer()
    annotations_dict = {}

    def __init__(self):
        annotations = self.create_annotation_dict()
        self.annotations_dict = {
            "RD": annotations['relativeDays'],
            "WD": annotations['weekDays'],
            "Month": annotations['months'],
            "Season": annotations['seasons'],
            "RT": annotations['relativeTime'],
            "TU": annotations['timeUnits'],
            "DU": annotations['dateUnits'],
            "Prev": annotations['prev'],
            "DP": annotations['dayPart'],
            "Next": annotations['next'],
            "SN": annotations['sixtyNum'],
            "HN": annotations['hoursNum'],
            "DN": annotations['dayNumbers'],
            "Hour": annotations['hours'],
            "Min": annotations['minute'],
            "Twelve": annotations['twelve'],
            "ThirtyOne": annotations['thirtyOne'],
            "RY": annotations['relativeYears'],
            "Num": annotations['numbers'],
            "PY": annotations["persianYear"]
            }

    def create_annotation_dict(self):
        annotation_dict = {}
        files = os.listdir(self.annotation_path)
        for f in files:
            key = f.replace('.txt', '')
            annotation_dict[key] = self.normalizer.normalize_annotation(f"{self.annotation_path}/{f}")

        annotation_dict['numbers'] = r'\\d{1,4}'

        ONE_TO_NINE_JOIN = "|".join(const.ONE_TO_NINE.keys())
        MAGNITUDE_JOIN = "|".join(const.MAGNITUDE.keys())
        HUNDREDS_TEXT_JOIN = "|".join(const.HUNDREDS_TEXT.keys())
        ONE_NINETY_NINE_JOIN = "|".join(list(const.ONE_NINETY_NINE.keys())[::-1])
        annotation_dict["persianYear"] = rf'(?:(?:{ONE_TO_NINE_JOIN})?\\s*(?:{MAGNITUDE_JOIN})?\\s*(?:{const.JOINER})?\\s*(?:{HUNDREDS_TEXT_JOIN})?\\s*(?:{const.JOINER})?\\s*(?:{ONE_NINETY_NINE_JOIN}))'
        return annotation_dict


class Patterns:
    annotations = {}
    normalizer = Normalizer()
    patterns_path = 'utilities/pattern'
    regexes = {}

    def __init__(self):
        self.annotations = Annotation()
        files = os.listdir(self.patterns_path)
        for f in files:
            self.regexes[f.replace('.txt', '')] = self.create_regexes_from_patterns(f"{self.patterns_path}/{f}")

    def pattern_to_regex(self, pattern):
        pattern = pattern.replace(" ", '+\\s')

        for key, value in self.annotations.annotations_dict.items():
            pattern = re.sub(f'{key}', "(?:" + value + ")", pattern)

        pattern = pattern + '+\\s'
        return pattern

    def create_regexes_from_patterns(self, path):
        patterns = self.normalizer.preprocess_file(path)
        regexes = [self.pattern_to_regex(pattern) for pattern in patterns]
        return regexes
