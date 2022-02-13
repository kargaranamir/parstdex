# parstdex (persian time date extractor) - پارس تی‌دِکس

## Pre-requisites
* This utility is written in Python 3. You will need a Python 3 interpreter installed or you will have to package this into a self contained executable. 

* This utility just uses builtin [re](https://docs.python.org/3/library/re.html). Therefore, you will not need to install any dependencies. 

## How to Install parstdex

```bash
pip install git+https://github.com/kargaranamir/parstdex
```

## How to Upgrade parstdex

```bash
pip install --upgrade git+https://github.com/kargaranamir/parstdex
```


## How to use (Examples)
```python
from parstdex import MarkerExtractor

# make a marker extractor object: this object will provide an environment for producing regexes and functions to process input text 
extractor = MarkerExtractor()

input_sentence = """ماریا شنبه عصر در ساعت نه و پنجاه نه دقیقه مورخ 13می 1999 با نادیا تماس گرفت اما نادیا بعدا در 1100/09/09 قمری به پرسش او پاسخ داد."""
print("Original Sentence:\n", input_sentence)
normalized_sentence, result = extractor.time_marker_extractor(input_sentence)

## Print results
print("Normalized Sentence:\n", normalized_sentence)
print("All Extracted Markers: ")
print(result)
for item in result:
    print(normalized_sentence[item[0]:item[1]])

```

```python
Original Sentence:
 ماریا شنبه عصر در ساعت نه و پنجاه نه دقیقه مورخ 13می 1999 با نادیا تماس گرفت اما نادیا بعدا در 1100/09/09 قمری به پرسش او پاسخ داد.
Normalized Sentence:
 ماریا شنبه عصر در ساعت نه و پنجاه نه دقیقه مورخ 13 می 1999 با نادیا تماس گرفت اما نادیا بعدا در 1100/09/09 قمری به پرسش او پاسخ داد.
All Extracted Markers: 
[(6, 15), (18, 43), (48, 59), (96, 112)]
شنبه عصر 
ساعت نه و پنجاه نه دقیقه 
13 می 1999 
```

## Acknowledgement
Initiation of this work came from this article and corresponding [repository](https://github.com/BehroozMansouri/ParsTime).
```
Mansouri, Behrooz, et al. "ParsTime: Rule-Based Extraction and Normalization of Persian Temporal Expressions." 
European Conference on Information Retrieval. Springer, Cham, 2018.
```

## Citation
If you use any part of this library in your research, please cite it using the following BibTex entry.
```
@misc{parstdex,
  author = {Kargaran, Amir Hossein and Mirzababaei, Sajad and Jahad, Hamid},
  title = {Parstdex: Persian Time Date Extractor Python Library},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/kargaranamir/parstdex}},
}
```
