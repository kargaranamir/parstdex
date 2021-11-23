from hazm import *
import re


def multiple_replace(dic, text):
    # to replace from a dict on the input text
    pattern = "|".join(map(re.escape, dic.keys()))
    return re.sub(pattern, lambda m: dic[m.group()], str(text))


def convert_to_en_or_at_least_fa(text):
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


sentence = " سلام 12157124 دو شنبه چهار شنبه 12 / بیست و دومین "
sentence = convert_to_en_or_at_least_fa(sentence)
sentence = normalize_hazm(sentence)
print(sentence)

def CustomTokenize():

    pass