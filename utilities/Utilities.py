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


JOINERS = ["و", " و "]


def multiple_replace(dic, text):
    # to replace from a dict on the input text
    pattern = "|".join(map(re.escape, dic.keys()))
    return re.sub(pattern, lambda m: dic[m.group()], str(text))


def conversion(text):
    dic = {
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
    return multiple_replace(dic, text)


def normalize_hazm(sentence):
    normalizer = Normalizer()
    normalizer.normalize(sentence)
    return sentence


def normalize_cumulative(sentence):
    sentence = conversion(sentence)
    sentence = normalize_hazm(sentence)
    return sentence



def convert_from_word(text):
    def tokenize(_text):
        slitted_text = _text.split(' ')
        slitted_text = [txt for txt in slitted_text if txt != JOINERS[0]]

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


# example
sentence = 'صد هزار و یک'
q = convert_from_word(sentence)
print(q)




