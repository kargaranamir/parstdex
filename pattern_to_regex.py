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
    main_path = 'annotation'
    files = os.listdir(main_path)
    for f in files:
        annotaion_dict[f.replace('.txt', '')] = normlize_annotaion(f"{main_path}/{f}")

    return annotaion_dict


def pattern_replace(pattern_str):
    replace_dict = {"num": annotaion_dict['numbers'], "Num": annotaion_dict['numbers'], "DP": annotaion_dict['dayPart'], "Day": annotaion_dict['days'], "RD": annotaion_dict['relativeDays'], "Next": annotaion_dict['next'], "Prev": annotaion_dict['past']}

    for key, value in replace_dict.items():
        pattern_str = pattern_str.replace(key, "(?:" + value + ")")
    pattern_str = pattern_str.replace(" ", '+\\s')
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
    main_path = 'pattern_test_time'
    files = os.listdir(main_path)
    for f in files:
        pattern_list = pattern_list + normlize_pattern(f"{main_path}/{f}")

    return pattern_list

annotaion_dict = annotaion()
# print(annotaion_dict.keys())
# s= re.findall(fr'\b(?:{annotaion_dict["daynumbers"]}?)\s', "glass watre 29 یک  دو سه بیست‌وسه لیوان ")
# print(s)

pattern_list = pattern()
# print(pattern_list[0])
#
# q= re.findall(fr'\b(?:ساعت+\s(?:{annotaion_dict["numbers"]})+\sو+\s(?:{annotaion_dict["numbers"]})+\sدقیقه+\sو+\s(?:{annotaion_dict["numbers"]}+\sثانیه?))', " ساعت یک و دو دقیقه و پنج ثانیه")
# print(q)
#
# q= re.findall(fr'\b(?:ساعت+\s(?:{annotaion_dict["numbers"]})+\sو+\s(?:{annotaion_dict["numbers"]})+\sدقیقه+\sو+\s(?:{annotaion_dict["numbers"]}+\sثانیه?))', " ساعت یک و دو دقیقه و پنج ثانیه")
# print(q)


for i in range(len(pattern_list)):
    u= re.findall(fr'\b(?:{pattern_list[i]})', "من با احمد ساعت یک و دو دقیقه و پنج ثانیه غروب به مکتب رفتم و در آنجا ساعت 15:13 شام خوردیم و به ساعت ماه نگاه کردیم")
    print(i, u)
