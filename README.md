# parstdex (persian time date extractor) - پارس تی‌دِکس

## Pre-requisites
* This utility is written in Python 3. You will need a Python 3 interpreter installed or you will have to package this into a self contained executable.

## How to Install parstdex

```bash
pip install parstdex
```

## How to Upgrade parstdex

```bash
pip install --upgrade parstdex
```

## How to use

```python
from parstdex import Parstdex

parstdex = Parstdex()

sentence = """ماریا شنبه عصر راس ساعت ۱۷ و بیست و سه دقیقه به نادیا زنگ زد اما تا سه روز بعد در تاریخ ۱۸ شهریور سال ۱۳۷۸ ه.ش. خبری از نادیا نشد"""
```
### Extract markers
```python
parstdex.extract_marker(sentence)
```
output :
```json
{"datetime": [[6, 47], [68, 78], [82, 111]], "date": [[6, 10], [68, 78], [82, 111]], "time": [[11, 47]]}
```
### Extract markers' value
```python
parstdex.extract_value(sentence)
```
output :
```json
[
   "17:23:00",
   "3 روز بعد",
   "1378/06/18"
]
```
### Extract markers' NER tags
```python
parstdex.extract_ner(sentence)
```
output :
```
[('ماریا', 'O'),
 ('شنبه', 'B-DAT'),
 ('عصر', 'I-DAT'),
 ('راس', 'I-DAT'),
 ('ساعت', 'I-DAT'),
 ('۱۷', 'I-DAT'),
 ('و', 'I-DAT'),
 ('بیست', 'I-DAT'),
 ('و', 'I-DAT'),
 ('سه', 'I-DAT'),
 ('دقیقه', 'I-DAT'),
 ('به', 'I-DAT'),
 ('نادیا', 'O'),
 ('زنگ', 'O'),
 ('زد', 'O'),
 ('اما', 'O'),
 ('تا', 'O'),
 ('سه', 'B-DAT'),
 ('روز', 'I-DAT'),
 ('بعد', 'I-DAT'),
 ('در', 'O'),
 ('تاریخ', 'B-DAT'),
 ('۱۸', 'I-DAT'),
 ('شهریور', 'I-DAT'),
 ('سال', 'I-DAT'),
 ('۱۳۷۸', 'I-DAT'),
 ('ه', 'I-DAT'),
 ('.', 'I-DAT'),
 ('ش', 'I-DAT'),
 ('.', 'I-DAT'),
 ('خبری', 'O'),
 ('از', 'O'),
 ('نادیا', 'O'),
 ('نشد', 'O')]

```


## File Structure:
Parstdex architecture is very flexible and scalable and therefore suggests an easy solution to adapt to new patterns which haven't been considered yet.
```

├── parstdex                 
│   └── utils
|   |   └── annotation
|   |   |   └── ...
|   |   └── pattern
|   |   |   └── ...
|   |   └── special_words
|   |   |   └── words.txt
|   |   └── const.py
|   |   └── normalizer.py
|   |   └── pattern_to_regex.py
|   |   └── spans.py
|   |   └── word_to_value.py
|   └── marker_extractor.py
└── Test           
│   └── data.json
|   └── test_parstdex.py
|      
└── examples.py
└── requirement.txt
└── settings.py
└── setup.py
```

## How to contribute

Please feel free to provide us with any feedback or suggestions.  You can find more information on how to contribute to Parstdex by reading the 
[contribution document](https://github.com/kargaranamir/parstdex/blob/main/contributing.md).

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
