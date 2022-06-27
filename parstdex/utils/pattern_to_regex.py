import re
import os
from parstdex.utils.normalizer import Normalizer
from parstdex.utils import const


def process_file(path):
    with open(path, 'r', encoding='utf-8-sig') as file:
        text = file.readlines()
        text = [x.rstrip() for x in text if not x.startswith('#') and len(x.strip()) > 0]  # remove \n
        return text


def get_special_words():
    lines = process_file(os.path.join(os.path.dirname(__file__), 'special_words/words.txt'))
    special_words = {}
    for line in lines:
        word, equal = line.strip().split(None, 1)
        special_words[word] = equal
    return special_words


class Annotation:
    """
    Annotation class is used to create annotation dictionary which will be used for creating regex from patterns
    in following steps.
    """

    path_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'annotation')

    time_annotation_path = os.path.join(path_dir, 'time', "")
    date_annotation_path = os.path.join(path_dir, 'date', "")
    aux_annotation_path = os.path.join(path_dir, 'ax', "")
    adv_annotation_path = os.path.join(path_dir, 'adv', "")

    annotations_dict = {}

    def __init__(self):
        # numbers annotation
        numbers_annotations = self.create_number_annotation_dict()
        # time annotation dictionary includes all annotations of time folder
        time_annotations = self.create_annotation_dict(self.time_annotation_path)
        # date annotation dictionary includes all annotations of date folder
        date_annotations = self.create_annotation_dict(self.date_annotation_path)
        # auxiliary annotation dictionary includes all annotations of auxiliary folder
        aux_annotations = self.create_annotation_dict(self.aux_annotation_path)
        # adversarial annotation dictionary includes all annotations of adversarial folder
        adv_annotations = self.create_annotation_dict(self.adv_annotation_path)

        self.annotations_dict = {**numbers_annotations,
                                 **time_annotations,
                                 **date_annotations,
                                 **aux_annotations,
                                 **adv_annotations}

    @staticmethod
    def create_annotation(path):
        text = process_file(path)
        annotation_mark = "|".join(text)
        return annotation_mark

    @staticmethod
    def create_number_annotation_dict():
        annotation_dict = {
            'NUM': r'\\d{1,4}|\\d{1}\.\\d{1}',  # all 1 to 4 digit numbers + decimal format 1 to 9
            'NY2': r'\\d{2}|\\d{4}',
            'N31': r'[0-2]?[0-9]|30|31',
            'N12': r'0?[0-9]|1[0-2]',
            'N24': r'[0-1]?[0-9]|2[0-4]',
            'N60': r'[0-5]?[0-9]',
            'N99': r'[0-9]{1,2}',
            'NY4': r'13[5-9][0-9]|140[0-9]|19[2-9][0-9]|20[0-2][0-9]',  # all Gregorian years
            'D99': rf'{const.DIGIT2}|{const.DIGIT1}',  # Persian alphabetic 2 digit numbers
            'DY4': const.DIGIT4,  # Persian alphabetic 4 digit numbers
            'DSMALL': rf"{const.DSMALL}",  # Persian alphabetic 1 to 4 digit numbers
            'DLARGE': const.DLARGE,  # All Persian supported numbers
        }

        return annotation_dict

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

        return annotation_dict


class Patterns:
    """
    Patterns class is used to create regexes corresponding to patterns defined in utilities/pattern folder.
    """
    __instance = None

    normalizer = Normalizer()
    regexes = {}
    cumulative_annotations = {}
    cumulative_annotations_keys = []

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Patterns.__instance is None:
            Patterns()
        return Patterns.__instance

    def __init__(self):
        if Patterns.__instance is None:
            annotations = Annotation()
            special_words = get_special_words()
            self.patterns_path = os.path.join(os.path.dirname(__file__), 'pattern', "")
            self.cumulative_annotations = {**annotations.annotations_dict, **special_words}
            for key, value in self.cumulative_annotations.items():
                self.cumulative_annotations[key] = value.replace("<>", r'(?:[\\s\\u200c]{0,3})').replace(" ", r'(?:[\\u200c\\s]{1,3})')
            self.cumulative_annotations_keys = sorted(self.cumulative_annotations, key=len, reverse=True)
            files = os.listdir(self.patterns_path)
            for f in files:
                self.regexes[f.replace('.txt', '').lower()] = self.create_regexes_from_patterns(f"{self.patterns_path}/{f}")

            self.regexes['space'] = [rf"\u200c+", rf"\s+"]
            Patterns.__instance = self
        else:
            Patterns.__instance = self

    def pattern_to_regex(self, pattern):
        """
        pattern_to_regex takes pattern and return corresponding regex
        :param pattern: str
        :return: str
        """
        annotation_keys = "|".join(self.cumulative_annotations_keys)
        matches = re.findall(annotation_keys, pattern)
        for key in matches:
            pattern = re.sub(f'{key}', fr"(?:{self.cumulative_annotations[key]})", pattern)

        pattern = pattern.replace(" ", r'(?:[\u200c\s]{1,3})')
        pattern = pattern.replace("<>", r'(?:[\s\u200c]{0,3})')
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
