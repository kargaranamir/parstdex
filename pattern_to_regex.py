import re
import os

def normlize_annotaion(path):
    with open(path, 'r') as file:
        annotaion_mark = file.readlines()
        annotaion_mark = annotaion_mark[1:] # first line is empty
        annotaion_mark = [x.rstrip() for x in annotaion_mark] # remove \n
        annotaion_mark = "|".join(annotaion_mark)

    return annotaion_mark

def annotaion():
    annotaion_dict = {}
    main_path = 'utilities/annotation'
    files = os.listdir(main_path)
    for f in files:
        annotaion_dict[f.replace('.txt', '')] = normlize_annotaion(f"{main_path}/{f}")

    #fix numbers: add more numbers 1 or 2 digits coverage
    annotaion_dict['numbers'] = annotaion_dict['numbers'] + '|\d{1,2}'

    return annotaion_dict


def pattern_replace(pattern_str):
    replace_dict = {"num": annotaion_dict['numbers'], "Num": annotaion_dict['numbers'], "DP": annotaion_dict['dayPart'], "Day": annotaion_dict['days'], "RD": annotaion_dict['relativeDays'], "Next": annotaion_dict['next'], "Prev": annotaion_dict['past']}

    for key, value in replace_dict.items():
        pattern_str = pattern_str.replace(key, "(?:" + value + ")")
    pattern_str = pattern_str.replace(" ", '+\\s+')
    return pattern_str


def normlize_pattern(path):
    pattern_marks = []
    with open(path, 'r') as file:
        pattern_marks = file.readlines()
        pattern_marks = pattern_marks[1:] # first line is empty
        pattern_marks = [x.rstrip() for x in pattern_marks] # remove \n
        pattern_marks = [pattern_replace(x) for x in pattern_marks]

    return pattern_marks

def pattern():
    pattern_list = []
    main_path = 'utilities/pattern'
    files = os.listdir(main_path)
    for f in files:
        pattern_list = pattern_list + normlize_pattern(f"{main_path}/{f}")

    return pattern_list

annotaion_dict = annotaion()
pattern_list = pattern()

# sample
sentence = "من با احمد ساعت یک و دو دقیقه و پنج ثانیه غروب به مکتب رفتم و در آنجا ساعت 51:51 شام خوردیم و به ساعت ماه نگاه کردیم همچنین علی ساعت 5 و ربع به ما ملحق شد و دقیقه‌ ای را نیز با او بودیم."
sentence = " ساعت 13  و بیست‌ودو دقیقه شده بود و صدای اذان به گوش می‌رسید"
for i in range(len(pattern_list)):
    u= re.findall(fr'\b(?:{pattern_list[i]})', sentence)
    print(i, ":", u)