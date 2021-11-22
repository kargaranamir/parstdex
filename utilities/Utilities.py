from hazm import *
import re

def custom_nomalize(sentenceInput):
    sentence = arabic_to_persian_number(sentenceInput)
    sentence = arabic_to_persian_character(sentence)
    normalized_date = DateNormalize(sentence)
    normalized_day = day_normalize(normalized_date) 


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
    return replacement(dic, sentence)

def CustomTokenize():

    pass

def day_normalize(sentence):
    temp = temp.split()
    lst = ['1', '2', '3', '4', '5',
           '۱', '۲', '۳', '۴', '۵',
           'یک', 'دو', 'سه', 'چهار', 'چار', 'پنج']
    if "شنبه" in temp:
        for x in range(len(temp)):
            if temp[x] == "شنبه" and temp[x-1] in lst:
                temp[x], temp[x-1] = temp[x-1]+temp[x], ""
    return temp   

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