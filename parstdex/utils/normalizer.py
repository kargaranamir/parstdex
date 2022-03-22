import re


class Normalizer:
    """
    Normalizer class is used to:
    - normalized arabic alphabet into persian alphabet(normalize_alphabet)
    """
    ALPHABET_DICT = {
        'ك': 'ک',
        'ى': 'ی',
        'ي': 'ی',
    }

    def normalize_alphabet(self, text):
        """
        normalizes arabic alphabet into persian alphabet
        :return:
        :type text: str
        """
        pattern = "|".join(map(re.escape, self.ALPHABET_DICT.keys()))
        return re.sub(pattern, lambda m: self.ALPHABET_DICT[m.group()], str(text))

    def normalize_cumulative(self, text: str) -> str:
        res = self.normalize_alphabet(text)
        return res
