import re


class Normalizer:
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
    C_NUMBERS = FA_NUMBERS + "|" + EN_NUMBERS

    @staticmethod
    def normalize_alphabet(self, text):
        pattern = "|".join(map(re.escape, self.ALPHABET_DICT.keys()))
        return re.sub(pattern, lambda m: self.ALPHABET_DICT[m.group()], str(text))

    @staticmethod
    def normalize_space(self, text):
        res = re.sub(fr'((?:{self.C_NUMBERS})+(\.(?:{self.C_NUMBERS})+)?)', r' \1 ', text)
        res = ' '.join(res.split())
        return res

    @staticmethod
    def normalize_cumulative(self, text):
        res = self.normlize_alphabet(text)
        res = self.normlize_space(res)
        return res
