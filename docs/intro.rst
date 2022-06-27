Getting Started!
================

How to Install parstdex
-----------------------

.. code:: bash

   pip install parstdex


How to use
----------

.. code:: python

   from parstdex import Parstdex

   model = Parstdex()

   sentence = """ماریا شنبه عصر راس ساعت ۱۷ و بیست و سه دقیقه به نادیا زنگ زد اما تا سه روز بعد در تاریخ ۱۸ شهریور سال ۱۳۷۸ ه.ش. خبری از نادیا نشد"""

Extract spans
~~~~~~~~~~~~~

.. code:: python

   model.extract_span(sentence)

output :

.. code:: json

   {"datetime": [[6, 47], [68, 78], [82, 111]], "date": [[6, 10], [68, 78], [82, 111]], "time": [[11, 47]]}

Extract markers
~~~~~~~~~~~~~~~

.. code:: python

   model.extract_marker(sentence)

.. code:: json

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

Extract TimeML scheme
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   model.extract_time_ml(sentence)

output :

.. code:: html

   ماریا
   <TIMEX3 type='DATE'>
   شنبه
   </TIMEX3>
   <TIMEX3 type='TIME'>
   عصر راس ساعت ۱۷ و بیست و سه دقیقه به
   </TIMEX3>
    نادیا زنگ زد اما
   <TIMEX3 type='DURATION'>
   تا سه روز بعد
   </TIMEX3>
    در
   <TIMEX3 type='DATE'>
   تاریخ ۱۸ شهریور سال ۱۳۷۸ ه.ش.
   </TIMEX3>
   خبری از نادیا نشد

Extract markers’ NER tags
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   model.extract_ner(sentence)

output :

::

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
