import re
import os
from parstdex.utils.normalizer import Normalizer
from parstdex.utils import const


def process_file(path):
    with open(path, 'r', encoding="utf8") as file:
        text = file.readlines()
        text = [x.rstrip() for x in text if not x.startswith('#') and len(x)>0]  # remove \n
        return text


def get_special_words():
    lines = process_file(os.path.join(os.path.dirname(__file__), 'special_words/words.txt'))
    special_words = {}
    for line in lines:
        word, equal = line.strip().split()
        special_words[word] = equal
    return special_words


class Annotation:
    """
    Annotation class is used to create annotation dictionary which will be used for creating regex from patterns
    in following steps.
    """
    time_annotation_path = os.path.join(os.path.dirname(__file__), 'annotation/time')
    date_annotation_path = os.path.join(os.path.dirname(__file__), 'annotation/date')
    aux_annotation_path = os.path.join(os.path.dirname(__file__), 'annotation/ax')

    annotations_dict = {}

    def __init__(self):
        # time annotation dictionary includes all annotations of time folder
        time_annotations = self.create_annotation_dict(self.time_annotation_path)
        # date annotation dictionary includes all annotations of date folder
        date_annotations = self.create_annotation_dict(self.date_annotation_path)
        # auxiliary annotation dictionary includes all annotations of auxiliary folder
        aux_annotations = self.create_annotation_dict(self.aux_annotation_path)

        self.annotations_dict = {**time_annotations, **date_annotations, **aux_annotations}

    @staticmethod
    def create_annotation(path):
        text = process_file(path)
        annotation_mark = "|".join(text)
        return annotation_mark

    def create_annotation_dict(self, annotation_path):
        """
        create_annotation_dict will read all annotation text files in utilities/annotations folder and
        create corresponding regex for the annotation folder
        :return: dict
        """
        annotation_dict = {}
        files = os.listdir(annotation_path)
        for f in files:
            key = f.replace('.txt', '')
            annotation_dict[key] = self.create_annotation(f"{annotation_path}/{f}")

        # all 1 to 4 digit numbers
        annotation_dict['NUM'] = r'\\d{1,4}'

        # supports persian numbers from one to four digits written with persian alphabet
        # example: سال هزار و سیصد و شصت و پنج
        ONE_TO_NINE_JOIN = "|".join(const.ONE_TO_NINE.keys())
        MAGNITUDE_JOIN = "|".join(const.MAGNITUDE.keys())
        HUNDREDS_TEXT_JOIN = "|".join(const.HUNDREDS_TEXT.keys())
        ONE_NINETY_NINE_JOIN = "|".join(list(const.ONE_NINETY_NINE.keys())[::-1])
        annotation_dict["PY"] = rf'(?:(?:{ONE_TO_NINE_JOIN})?\\s*(?:{MAGNITUDE_JOIN})?\\s*(?:{const.JOINER})?\\s*(?:{HUNDREDS_TEXT_JOIN})?\\s*(?:{const.JOINER})?\\s*(?:{ONE_NINETY_NINE_JOIN}))'

        return annotation_dict


class Patterns:
    """
    Patterns class is used to create regexes corresponding to patterns defined in utilities/pattern folder.
    """
    annotations = {}
    normalizer = Normalizer()
    patterns_path = os.path.join(os.path.dirname(__file__), 'pattern')
    regexes = {}
    special_words = {}

    def __init__(self):
        self.annotations = Annotation()
        self.special_words = get_special_words()
        files = os.listdir(self.patterns_path)
        for f in files:
            self.regexes[f.replace('.txt', '')] = self.create_regexes_from_patterns(f"{self.patterns_path}/{f}")

    def pattern_to_regex(self, pattern):
        """
        pattern_to_regex takes pattern and return corresponding regex
        :param pattern: str
        :return: str
        """
        pattern = pattern.replace(" ", '+\\s')
        for key, value in self.annotations.annotations_dict.items():
            for word, equal in self.special_words.items():
                pattern = pattern.replace(word, equal)
            pattern = re.sub(f'{key}', "(?:" + value + ")", pattern)

        pattern = pattern + '+\\s'
        return pattern

    def create_regexes_from_patterns(self, path):
        """
        create_regexes_from_patterns takes path of pattern folder and return list of regexes corresponding to
        pattern folder.
        :param path: str
        :return: list
        """
        patterns = process_file(path)
        regexes = [self.pattern_to_regex(pattern) for pattern in patterns]
        return regexes

