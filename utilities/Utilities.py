from hazm import *
import re

def custom_nomalize(sentenceInput):
    sentence = arabic_to_persian_number(sentenceInput)
    sentence = arabic_to_persian_character(sentence)
    normalized_date = DateNormalize(sentence)


def DateNormalize(sentence):
    # match = re.search(r'(\d+\s+/\s+\d+\s+/\s+\d+)','The date is 11/ 12/98')
    dic = {
        "/ ": "/",
        " /": "/",
        "- ": "-",
        " -": "-",
        ": ": ":",
        " :": ":"
    }
    # match = sentence.replace("/ ", "/")
    # match = match.replace(" /", "/")
    # match = match.replace("- ", "-")
    # match = match.replace(" -", "-")
    # match = match.replace(" :", ":")
    # match = match.replace(": ", ":")
    
    return replacement(dic, sentence)

def CustomTokenize():

    pass

def arabic_to_persian_number(number):
    dic = {
        '١': '۱',
        '٢': '۲',
        '٣': '۳',
        '٤': '۴',
        '٥': '۵',
        '٦': '۶',
        '٧': '۷',
        '٨': '۸',
        '٩': '۹',
        '٠': '۰',
        }
    return replacement(dic, number)

def arabic_to_persian_character(userInput):
    dic = {
        'ك': 'ک',
        'دِ': 'د',
        'بِ': 'ب',
        'زِ': 'ز',
        'ذِ': 'ذ',
        'شِ': 'ش',
        'سِ': 'س',
        'ى': 'ی',
        'ي': 'ی'
        }
    return replacement(dic, userInput)

def replacement(dic, text):
    pattern = "|".join(map(re.escape, dic.keys()))
    return re.sub(pattern, lambda m: dic[m.group()], str(text))