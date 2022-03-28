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
        word, equal = line.strip().split()
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
            'NUM': r'\\d{1,4}',  # all 1 to 4 digit numbers
            'PN': const.PN  # Persian alphabetic numbers
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
    normalizer = Normalizer()
    regexes = {}
    cumulative_annotations = {}
    cumulative_annotations_keys = []

    def __init__(self):
        annotations = Annotation()
        special_words = get_special_words()
        self.patterns_path = os.path.join(os.path.dirname(__file__), 'pattern', "")
        self.cumulative_annotations = {**annotations.annotations_dict, **special_words}
        self.cumulative_annotations_keys = sorted(self.cumulative_annotations, key=len, reverse=True)
        files = os.listdir(self.patterns_path)
        for f in files:
            self.regexes[f.replace('.txt', '').lower()] = self.create_regexes_from_patterns(f"{self.patterns_path}/{f}")

        self.regexes['Space'] = [rf"\u200c+", rf"\s+"]

    def pattern_to_regex(self, pattern):
        """
        pattern_to_regex takes pattern and return corresponding regex
        :param pattern: str
        :return: str
        """
        # TODO: WHY \s*
        pattern = pattern.replace(" ", r'\s*')
        annotation_keys = "|".join(self.cumulative_annotations_keys)
        matches = re.findall(annotation_keys, pattern)
        for key in matches:
            pattern = re.sub(f'{key}', fr"(?:{self.cumulative_annotations[key]})", pattern)

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
