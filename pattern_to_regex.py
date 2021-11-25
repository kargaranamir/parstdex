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
    annotation_dict['numbers'] = r'\\d{1,4}'

    return annotation_dict


def pattern_replace(pattern_str):
    res_annotation_dict = annotation()
    replace_dict = {"RD": res_annotation_dict['relativeDays'],
                    "Day": res_annotation_dict['days'],
                    "Month": res_annotation_dict['months'],
                    "Season": res_annotation_dict['seasons'],
                    "RT": res_annotation_dict['relativeDays'],
                    "TU": res_annotation_dict['timeUnits'],
                    "Prev": res_annotation_dict['past'],
                    "DP": res_annotation_dict['dayPart'],
                    "Next": res_annotation_dict['next'],
                    "SixtyNum": res_annotation_dict['sixtyNum'],
                    "HourNum": res_annotation_dict['hoursNum'],
                    "DN": res_annotation_dict['dayNumbers'],
                    "Hour": res_annotation_dict['hours'],
                    "Min": res_annotation_dict['minute'],
                    "Twelve": res_annotation_dict['twelve'],
                    "ThirtyOne": res_annotation_dict['thirtyOne'],
                    "RY": res_annotation_dict['relativeYears'],
                    "Num": res_annotation_dict['numbers']
                    }

    # replace_dict = {
    #     "Twelve": res_annotation_dict['twelve'],
    #     "ThirtyOne": res_annotation_dict['thirtyOne'],
    #     "Num": res_annotation_dict['numbers']
    # }

    pattern_str = pattern_str.replace(" ", '+\\s')
    for key, value in replace_dict.items():
        pattern_str = re.sub(f'{key}', "(?:" + value + ")", pattern_str)

    pattern_str = pattern_str + '+\\s'
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