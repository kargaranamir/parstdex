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
    time_annotation_path = os.path.join(os.path.dirname(__file__), 'annotation/time')
    date_annotation_path = os.path.join(os.path.dirname(__file__), 'annotation/date')
    aux_annotation_path = os.path.join(os.path.dirname(__file__), 'annotation/ax')
    adv_annotation_path = os.path.join(os.path.dirname(__file__), 'annotation/adv')

    annotations_dict = {}

    def __init__(self):
        # time annotation dictionary includes all annotations of time folder
        time_annotations = self.create_annotation_dict(self.time_annotation_path)
        # date annotation dictionary includes all annotations of date folder
        date_annotations = self.create_annotation_dict(self.date_annotation_path)
        # auxiliary annotation dictionary includes all annotations of auxiliary folder
        aux_annotations = self.create_annotation_dict(self.aux_annotation_path)
        # adversarial annotation dictionary includes all annotations of adversarial folder
        adv_annotations = self.create_annotation_dict(self.adv_annotation_path)

        self.annotations_dict = {**time_annotations,
                                 **date_annotations,
                                 **aux_annotations,
                                 **adv_annotations}

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
        # example:  هزار و سیصد و شصت و پنج
        ONE_TO_NINE_JOIN = "|".join(const.ONE_TO_NINE.keys())
        MAGNITUDE_JOIN = "|".join(const.MAGNITUDE.keys())
        HEZAR = "هزار"
        HUNDREDS_TEXT_JOIN = "|".join(const.HUNDREDS_TEXT.keys())
        ONE_NINETY_NINE_JOIN = "|".join(list(const.ONE_NINETY_NINE.keys())[::-1])
        NIM_SPACE = '\u200c'
        WHITE_SPACE = rf'[{NIM_SPACE}\\s]'

        PN1 = rf"(?:{ONE_TO_NINE_JOIN})"

        PNDAH = rf"(?:{ONE_NINETY_NINE_JOIN})"
        PN1DAH = rf"{PNDAH}{WHITE_SPACE}*(?:{const.JOINER}){WHITE_SPACE}*" + PN1
        PN2 = PN1DAH + "|" + PNDAH

        PNSAD = rf"(?:{HUNDREDS_TEXT_JOIN})"
        PN2SAD = rf"{PNSAD}{WHITE_SPACE}*(?:{const.JOINER}){WHITE_SPACE}*" + "(?:" + PN2 + "|" + PN1 + ")"
        PN3 = PN2SAD + "|" + PNSAD

        PNHEZAR = rf"{HEZAR}"
        PN1HEZAR = "(?:" + PN3 + "|" + PN2 + "|" + PN1 + ")" + rf"{WHITE_SPACE}*{PNHEZAR}"
        PN2HEZAR = rf"{PNHEZAR}{WHITE_SPACE}*(?:{const.JOINER}){WHITE_SPACE}*" + "(?:" + PN3 + "|" + PN2 + "|" + PN1 + ")"
        PN3HEZAR = rf"{PN1HEZAR}{WHITE_SPACE}*(?:{const.JOINER}){WHITE_SPACE}*" + "(?:" + PN3 + "|" + PN2 + "|" + PN1 + ")"
        PN4 = PN3HEZAR + "|" + PN2HEZAR + "|" + PN1HEZAR + "|" + PNHEZAR

        # TODO: support larger numbers
        MAGNITUDES = MAGNITUDE_JOIN

        PN = PN4 + "|" + PN3 + "|" + PN2 + "|" + PN1 + "|" + MAGNITUDES
        annotation_dict["PN"] = PN

        return annotation_dict


class Patterns:
    """
    Patterns class is used to create regexes corresponding to patterns defined in utilities/pattern folder.
    """
    annotations = {}
    normalizer = Normalizer()
    regexes = {}
    special_words = {}

    def __init__(self):
        self.annotations = Annotation()
        self.special_words = get_special_words()
        self.patterns_path = os.path.join(os.path.dirname(__file__), 'pattern')
        files = os.listdir(self.patterns_path)
        for f in files:
            self.regexes[f.replace('.txt', '')] = self.create_regexes_from_patterns(f"{self.patterns_path}/{f}")

        self.regexes['Space'] = [rf"\u200c+", rf"\s+"]

    def pattern_to_regex(self, pattern):
        """
        pattern_to_regex takes pattern and return corresponding regex
        :param pattern: str
        :return: str
        """
        pattern = pattern.replace(" ", r'\s*')
        final_annotations = {**self.annotations.annotations_dict, **self.special_words}
        final_annotations_keys = sorted(final_annotations, key=len, reverse=True)
        for key in final_annotations_keys:
            pattern = re.sub(f'{key}', fr"(?:{final_annotations[key]})", pattern)

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
