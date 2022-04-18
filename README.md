# parstdex (persian time date extractor) - پارس تی‌دِکس

[![Pypi Package](https://badgen.net/pypi/v/parstdex)](https://pypi.org/project/parstdex/)
[![Documentation Status](https://readthedocs.org/projects/parstdex/badge/?version=latest)](https://parstdex.readthedocs.io)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/kargaranamir/parstdex)
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kargaranamir/parstdex/blob/main/performance_test.ipynb)

## How to Install parstdex

```bash
pip install parstdex
```

## How to use

```python
from parstdex import Parstdex

model = Parstdex()

sentence = """ماریا شنبه عصر راس ساعت ۱۷ و بیست و سه دقیقه به نادیا زنگ زد اما تا سه روز بعد در تاریخ ۱۸ شهریور سال ۱۳۷۸ ه.ش. خبری از نادیا نشد"""
```
### Extract spans
```python
model.extract_span(sentence)
```
output :
```json
{"datetime": [[6, 47], [68, 78], [82, 111]], "date": [[6, 10], [68, 78], [82, 111]], "time": [[11, 47]]}
```

### Extract markers
```python
model.extract_marker(sentence)
```

```json
{
   "datetime":{
      "[6, 47]":"شنبه عصر راس ساعت ۱۷ و بیست و سه دقیقه به",
      "[68, 78]":"سه روز بعد",
      "[82, 111]":"تاریخ ۱۸ شهریور سال ۱۳۷۸ ه.ش."
   },
   "date":{
      "[6, 10]":"شنبه",
      "[68, 78]":"سه روز بعد",
      "[82, 111]":"تاریخ ۱۸ شهریور سال ۱۳۷۸ ه.ش."
   },
   "time":{
      "[11, 47]":"عصر راس ساعت ۱۷ و بیست و سه دقیقه به"
   }
}
```

### Extract markers' value
```python
model.extract_value(sentence)
```
output :
```json
{
   "date":{
      "[6, 10]":"شنبه",
      "[68, 78]":"3 روز بعد",
      "[82, 111]":"1378/06/18"
   },
   "time":{
      "[11, 47]":"17:23:00"
   }
}
```
### Extract markers' NER tags
```python
model.extract_ner(sentence)
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
|   └── settings.py
└── Test           
│   └── data.json
|   └── test_parstdex.py
|      
└── examples.py
└── performance_test.ipynb
└── requirement.txt
└── setup.py
```

## Performance Test 
Executable codes and performance test results are accessible on [google colab](https://colab.research.google.com/github/kargaranamir/parstdex/blob/main/performance_test.ipynb).

The average time required to obtain temporal expressions is `6 ms`. This test was conducted using 264 sentences with an average length of 50 characters that covered all of the patterns.

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
