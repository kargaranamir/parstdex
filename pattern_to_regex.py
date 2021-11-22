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


annotaion_dict = annotaion()


s= re.findall(fr'\b(?:{annotaion_dict["daynumbers"]}?)\s', "glass watre 29 یک  دو سه بیست‌وسه لیوان ")
print(s)