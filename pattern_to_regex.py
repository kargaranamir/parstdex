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
        annotaion_dict[f.rstrip('.txt')] = normlize_annotaion(f"{main_path}/{f}")

    return annotaion_dict


def pattern_replace(pattern_str):
    replace_dict = {"num": "{numbers}", "Num": "{numbers}", "DP": "{dayPart}", "Day": "{days}", "RD": "{relativeDays}", "Next": "{next}", "Prev": "{past}"}

    for key, value in replace_dict.items():
        pattern_str = pattern_str.replace(key, value)

    pattern_str = "fr'\b(?:" + pattern_str + "?)"
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
s= re.findall(fr'\b(?:{annotaion_dict["daynumbers"]}?)\s', "glass watre 29 یک  دو سه بیست‌وسه لیوان ")
print(s)

pattern_list = pattern()
print(pattern_list)