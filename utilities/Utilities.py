from typing import Dict

from hazm import *
import re

ONES_TEXT = {
    'صفر': 0,
    'یک': 1,
    'دو': 2,
    'سه': 3,
    'چهار': 4,
    'پنج': 5,
    'شش': 6,
    'شیش': 6,
    'هفت': 7,
    'هشت': 8,
    'نه': 9,
    'ده': 10
}

TENS_TEXT = {
    'بیست': 20,
    'سی': 30,
    'چهل': 40,
    'پنجاه': 50,
    'شصت': 60,
    'هفتاد': 70,
    'هشتاد': 80,
    'نود': 90,
}

TEN_PLUS_TEXT: Dict[str, int] = {
    'یازده': 11,
    'دوازده': 12,
    'سیزده': 13,
    'چهارده': 14,
    'پانزده': 15,
    'شانزده': 16,
    'هفده': 17,
    'هجده': 18,
    'نوزده': 19,
}

HUNDREDS_TEXT = {
    'یکصد': 100,
    'صد': 100,
    'دویست': 200,
    'سیصد': 300,
    'چهارصد': 400,
    'پانصد': 500,
    'ششصد': 600,
    'شیشصد': 600,
    'هفتصد': 700,
    'هشتصد': 800,
    'نهصد': 900,
}


MAGNITUDE = {
    'هزار': 1000,
    'میلیون': 1000000,
    'بیلیون': 1000000000,
    'میلیارد': 1000000000,
    'تریلیون': 1000000000000,
}

TYPO_LIST = {
    'شیش صد': 'ششصد',
    'شش صد': 'ششصد',
    'هفت صد': 'هفتصد',
    'هشت صد': 'هشتصد',
    'نه صد': 'نهصد',
}

ALPHABET_DICT = {
    '١': '1',
    '٢': '2',
    '٣': '3',
    '٤': '4',
    '٥': '5',
    '٦': '6',
    '٧': '7',
    '٨': '8',
    '٩': '9',
    '٠': '0',
    '۱': '1',
    '۲': '2',
    '۳': '3',
    '۴': '4',
    '۵': '5',
    '۶': '6',
    '۷': '7',
    '۸': '8',
    '۹': '9',
    '۰': '0',
    'ك': 'ک',
    'دِ': 'د',
    'بِ': 'ب',
    'زِ': 'ز',
    'ذِ': 'ذ',
    'شِ': 'ش',
    'سِ': 'س',
    'ى': 'ی',
    'ي': 'ی',
    '/ ': '/',
    '- ': '-',
    ' -': '-',
    ' :': ':',
    ': ': ':'
}

JOINER = 'و'

Units = "|".join(list(ONES_TEXT.keys()) + list(TENS_TEXT.keys()) + list(TEN_PLUS_TEXT.keys()) + list(HUNDREDS_TEXT.keys()) + list(MAGNITUDE.keys()) + list(TYPO_LIST.keys()))


def normlize_alphabet(text):
    pattern = "|".join(map(re.escape, ALPHABET_DICT.keys()))
    return re.sub(pattern, lambda m: ALPHABET_DICT[m.group()], str(text))


def normalize_hazm(sentence):
    normalizer = Normalizer()
    normalizer.normalize(sentence)
    return sentence


def convert_word_to_digits(text):
    def tokenize(_text):
        for typo in TYPO_LIST.keys():
            if typo in _text:
                _text = _text.replace(typo, TYPO_LIST[typo])
        slitted_text = _text.split(' ')
        slitted_text = [txt for txt in slitted_text if txt != JOINER]

        return slitted_text

    def remove_ordinal_suffix(word: str) -> str:
        word = word.replace('مین', '')
        word = word.replace(' ام', '')
        word = word.replace(' اُم', '')

        if word.endswith('سوم'):
            return word[:-3] + 'سه'
        elif word.endswith('م'):
            return word[:-1]
        return word

    def compute(tokens):
        result = 0

        for token in tokens:
            if ONES_TEXT.get(token):
                result += ONES_TEXT[token]
            if TEN_PLUS_TEXT.get(token):
                result += TEN_PLUS_TEXT[token]
            if TENS_TEXT.get(token):
                result += TENS_TEXT[token]
            elif HUNDREDS_TEXT.get(token):
                result += HUNDREDS_TEXT[token]
            elif token.isdigit():
                result += int(token)
            elif MAGNITUDE.get(token):
                result *= MAGNITUDE[token]

        return result

    if text == '' or text is None:
        return None

    text = remove_ordinal_suffix(text)

    computed = compute(tokenize(text))
    return computed


def normalize_digits(sentence):
    normlized_output = re.sub(fr'(?:{Units}|{JOINER}|\s|\d)+', lambda m: str(convert_word_to_digits(m.group())), sentence)
    return normlized_output

def normalize_cumulative(sentence):
    sentence = normlize_alphabet(sentence)
    sentence = normalize_hazm(sentence)
    # sentence = normalize_digits(sentence)
    return sentence

#sample
sentence = 'صد و شش امیر و یک هزار و هفت'
q = normalize_digits(sentence)
print(q)