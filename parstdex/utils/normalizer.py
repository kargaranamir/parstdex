import re


class Normalizer:
    """
    Normalizer class is used to:
    - normalized arabic alphabet into persian alphabet(normalize_alphabet)
    - normalize space - digit to word concatenation - comma and other spacial symbols
    - normalize_annotation method is used to normalize annotation files in utilities/annotation folder
    - normalize_cumulative method execute normalize alphabet and space consequently
    """
    ALPHABET_DICT = {
        'ك': 'ک',
        'دِ': 'د',
        'بِ': 'ب',
        'زِ': 'ز',
        'ذِ': 'ذ',
        'شِ': 'ش',
        'سِ': 'س',
        'ى': 'ی',
        'ي': 'ی',
    }

    FA_NUMBERS = "۰|۱|۲|۳|۴|۵|۶|۷|۸|۹"
    EN_NUMBERS = "0|1|2|3|4|5|6|7|8|9"
    Symbols = ":|/|-|\."
    C_NUMBERS = FA_NUMBERS + "|" + EN_NUMBERS + "|" + Symbols

    def normalize_alphabet(self, text):
        pattern = "|".join(map(re.escape, self.ALPHABET_DICT.keys()))
        return re.sub(pattern, lambda m: self.ALPHABET_DICT[m.group()], str(text))

    @staticmethod
    def normalize_space(text):
        # Remove persian comma
        res = text.replace('،', ' ')
        # Remove parenthesis
        res = re.sub(r"\(|\)", " ", res)
        return res

    def normalize_cumulative(self, text):
        res = self.normalize_alphabet(text)
        res = self.normalize_space(res)
        return res
