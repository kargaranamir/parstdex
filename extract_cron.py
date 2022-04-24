import enum
from parstdex.utils.word_to_value import ValueExtractor
from parstdex.utils import const
from parstdex.utils.pattern_to_regex import Patterns
import re


class StatementType(enum.Enum):
    EXACT_TIME = 1,
    DURATION = 2,
    CRON = 3,

def is_cron(text: str) -> bool:
    return text.startswith('هر') or 'ها ' in text

def decide_type(markers: dict) -> StatementType:
    cron = all(map(is_cron, markers['datetime'].values()))
    return StatementType.CRON

    if cron:
        return StatementType.CRON
    return StatementType.DURATION


SECOND_CRON_REGEX = "ثانیه"


CRON_LITERAL = 'هر'

# const.MINUTES
# ValueExtractor.SEC_LIT
# const.DLARGE
# Patterns.getInstance().regexes['time']

space = Patterns.getInstance().regexes['Space']
WD = Patterns.getInstance().cumulative_annotations['WD']
CJ = Patterns.getInstance().cumulative_annotations['CJ']
print(Patterns.getInstance().regexes.keys())
time = Patterns.getInstance().regexes['time']

minute_literal = rf"(?P<minute_lieral>{ValueExtractor.MIN_LIT})"
hour_literal = rf"(?P<minute_lieral>{ValueExtractor.MIN_LIT})"

minute_and_hour_literals = rf"(?P<minute_and_hour_literals>{ValueExtractor.MIN_LIT}|{ValueExtractor.HOUR_LIT})"
day = rf"(?P<day>{WD})"
simple_day_range = rf"(?P<from_day>{WD}){space}(?:{CJ}){space}(?P<to_day>{WD})"
day_range = rf"(?P<day_range>{simple_day_range})"
days = rf"(?P<days>{day_range}|{day})"
time_combined = "(" + ")|(".join(time) + ")"



pattern1 = rf"{CRON_LITERAL}{space}(?:(?P<value>{const.DLARGE}){space})?{minute_and_hour_literals}"
pattern2 = rf"{CRON_LITERAL}{space}({days})?{space}(?P<time>{time_combined})"                     # "هر یه تعدادی روز ساعت"
patterns = [eval(f'pattern{i}') for i in range(1,3)]


def extract_cron(markers, values):
    assert decide_type(markers) == StatementType.CRON
    
    print("\n" * 10)
    print(markers)
    print(values)

    s = markers['datetime']

    for pattern in patterns:
        print(pattern, s)
        m = re.match(pattern, s)
        if m:
            return m

    return None


def test_time():
    ve = ValueExtractor()
    z = "ساعت ۵ و پنجاه و هشت دقیقه شب"
    z = "ساعت ۵ عصر ژانویه"
    z = "۲۰ دقیقه مانده به شیش عصر"
    z = "ساعت ۷ و سی ۱ ثانیه"
    z = "ده صبح"
    z = "۶:۱۷ صبح"
    x = ve.compute_value(z)
    y = ve.compute_time_value(z)
    print(x)
    print(y)

def test_date():
    ve = ValueExtractor()
    z = "دوشنبه تا چهارشنبه پنج فروردین"
    z = "پنج فروردین"
    z = "پنج فروردین سال ۱۴۰۰"
    x = ve.compute_date_value(z)
    print(x)


def verify_day():
    s1 = "دو شنبه"
    m = re.match(day, s1)
    assert m is not None
    s2 = "سه مبه" 
    m = re.match(day, s2)
    assert m is None


def verify_simple_day_range():
    print(space)
    s1 = "شنبه تا سه‌شنبه"
    m = re.match(simple_day_range, s1)
    assert m is not None
    d = m.groupdict()
    assert d['from_day'] == 'شنبه'
    assert d['to_day'] == 'سه‌شنبه'

def verify_day_range():
    s1 = "شنبه تا سه‌شنبه"
    m = re.match(day_range, s1)
    assert m is not None
    d = m.groupdict()
    
    assert d['from_day'] == 'شنبه'
    assert d['to_day'] == 'سه‌شنبه'
    assert d['day_range'] == s1
    

def verify_days():
    s1 = "شنبه لغایت آدینه"
    m = re.match(days, s1)
    assert m is not None
    
    d = m.groupdict()
    
    assert d['days'] == s1
    assert d['day_range'] == s1
    assert d['from_day'] == 'شنبه'
    assert d['to_day'] == 'آدینه'
    assert d['day'] is None


def verify_time():
    s1 = "ساعت پنج عصر"
    m = re.match(time_combined, s1)
    assert m is not None

    s2 = "ساعت ۱۷"
    m = re.match(time_combined, s1)
    assert m is not None


def verify_regexes():
    verify_day()
    verify_simple_day_range()
    verify_day_range()
    verify_days()
    verify_time()


def verify_pattern1():
    s1 = "هر دقیقه"
    m = re.match(pattern1, s1)
    assert m is not None
    d = m.groupdict()

    assert d['minute_and_hour_literals'] == 'دقیقه'
    assert d['value'] == None


def verify_pattern2():
    s1 =  'هر پنجشنبه تا جمعه ساعت ۱۷'""
    m = re.match(pattern2, s1)
    assert m is not None



def verify_patterns():
    verify_pattern1()
    verify_pattern2()


if __name__ == "__main__":
    # test_time()
    # test_date()
    verify_regexes()
    verify_patterns()
    