import re
import os


def normalize_annotation(path):
    with open(path, 'r', encoding="utf8") as file:
        annotation_mark = file.readlines()
        annotation_mark = annotation_mark[1:]  # first line is empty
        annotation_mark = [x.rstrip() for x in annotation_mark]  # remove \n
        annotation_mark = "|".join(annotation_mark)

    return annotation_mark


def annotation():
    annotation_dict = {}
    main_path = 'utilities/annotation'
    files = os.listdir(main_path)
    for f in files:
        annotation_dict[f.replace('.txt', '')] = normalize_annotation(f"{main_path}/{f}")

    # fix numbers: add more numbers 1 or 2 digits coverage
    annotation_dict['numbers'] = annotation_dict['numbers'] + r'|\d{1,2}'

    return annotation_dict


def pattern_replace(pattern_str):
    res_annotation_dict = annotation()
    replace_dict = {"num": res_annotation_dict['numbers'],
                    "Num": res_annotation_dict['numbers'],
                    "DP": res_annotation_dict['dayPart'],
                    "Day": res_annotation_dict['days'],
                    "RD": res_annotation_dict['relativeDays'],
                    "Next": res_annotation_dict['next'],
                    "Prev": res_annotation_dict['past']
                    }

    for key, value in replace_dict.items():
        pattern_str = pattern_str.replace(key, "(?:" + value + ")")
    pattern_str = pattern_str.replace(" ", '+\\s')
    return pattern_str


def normalize_pattern(path):
    with open(path, 'r', encoding="utf8") as file:
        pattern_marks = file.readlines()
        pattern_marks = pattern_marks[1:]  # first line is empty
        pattern_marks = [x.rstrip() for x in pattern_marks]  # remove \n
        pattern_marks = [pattern_replace(x) for x in pattern_marks]

    return pattern_marks


def pattern():
    pattern_list = []
    main_path = 'utilities/pattern'
    files = os.listdir(main_path)
    for f in files:
        pattern_list = pattern_list + normalize_pattern(f"{main_path}/{f}")

    return pattern_list


res_pattern_list = pattern()

# sample
sentence = "من با احمد ساعت یک و دو دقیقه و پنج ثانیه غروب به مکتب رفتم و در آنجا ساعت 51:51 شام خوردیم و به ساعت ماه نگاه کردیم همچنین علی ساعت 5 و ربع به ما ملحق شد و دقیقه‌ ای را نیز با او بودیم."

for i in range(len(res_pattern_list)):
    u = re.findall(fr'\b(?:{res_pattern_list[i]})', sentence)
    print(i, ":", u)
