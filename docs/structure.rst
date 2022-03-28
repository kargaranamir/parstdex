File Structure
==============

Parstdex architecture is very flexible and scalable and therefore
suggests an easy solution to adapt to new patterns which haven’t been
considered yet.

::


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
   └── requirement.txt
   └── setup.py
