import re


class Normalizer:
    """
    Normalizer class is used to:
    - preprocess input files(preprocess_file)
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
    Symbols = ":|/|-"
    C_NUMBERS = FA_NUMBERS + "|" + EN_NUMBERS + "|" + Symbols

    def normalize_alphabet(self, text):
        pattern = "|".join(map(re.escape, self.ALPHABET_DICT.keys()))
        return re.sub(pattern, lambda m: self.ALPHABET_DICT[m.group()], str(text))

    def normalize_space(self, text):
        res = text.replace('،', '')
        res = ':'.join([i.lstrip().rstrip() for i in res.split(':')])
        res = '-'.join([i.lstrip().rstrip() for i in res.split('-')])
        res = '/'.join([i.lstrip().rstrip() for i in res.split('/')])
        res = '/'.join([i.lstrip().rstrip() for i in res.split('\\')])
        res = re.sub(fr'((?:{self.C_NUMBERS})+(\.(?:{self.C_NUMBERS})+)?)', r' \1 ', res)
        # res = res.replace('\u200c', '')
        res = ' '.join(res.split())
        res = res + ' .' if res[-1] != '.' else res
        return res

    @staticmethod
    def preprocess_file(path):
        with open(path, 'r', encoding="utf8") as file:
            text = file.readlines()
            text = text[1:]  # first line is empty
            text = [x.rstrip() for x in text]  # remove \n
            return text

    def normalize_annotation(self, path):
        text = self.preprocess_file(path)
        annotation_mark = "|".join(text)
        return annotation_mark

    def normalize_cumulative(self, text):
        res = self.normalize_alphabet(text)
        res = self.normalize_space(res)
        return res


def deleteSubMatches(matches, matches_keys, input_sentence):
    """
    deleteSubMatches method deletes matches which are considered to be subset of another match
    :param matches: list
    :param matches_keys: list
    :param input_sentence: str
    :return: list
    """
    def is_sub_match(word, match_list):
        """
        is_sub_match checks if word is subset of any strings in match_list or not
        :param word: str
        :param match_list: list
        :return: boolean
        """
        for match in match_list:
            if word in match and word != match:
                return True
        return False

    unique_matches = []
    unique_matches_keys = []
    other_matches = []
    other_matches_keys = []

    for match_key, match in zip(matches_keys, matches):
        if not is_sub_match(match, matches):
            unique_matches.append(match)
            unique_matches_keys.append(match_key)

    for match_key, match in zip(matches_keys, matches):
        if match in matches and match not in unique_matches:
            other_matches.append(match)
            other_matches_keys.append(match_key)

    sub_words = []
    for u_match in unique_matches:
        if u_match in input_sentence:
            input_sentence = input_sentence.replace(u_match, ' $ ')
        else:
            sub_words.append(u_match)

    # extra delete
    for s_match in sub_words:
        for sub_match in s_match.split(' '):
            input_sentence = input_sentence.replace(sub_match, ' $ ')

    for p_match_key, p_match in zip(other_matches_keys, other_matches):
        if p_match in input_sentence:
            unique_matches.append(p_match)
            unique_matches_keys.append(p_match_key)

    keys = list(set(matches_keys))
    matches_dict = {}
    for k in keys:
        matches_dict[k]: list = []

    for key, value in zip(unique_matches_keys, unique_matches):
        matches_dict[key].append(value)

    return matches_dict
