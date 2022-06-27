from calendar import week
import enum
from parstdex.utils import word_to_value
from parstdex.utils.normalizer import Normalizer
from parstdex.utils.word_to_value import ValueExtractor
from parstdex.utils import const
from parstdex.utils.pattern_to_regex import Patterns
import re

HAR_LITERAL = 'هر'
HA_LITERAL = 'ها'

space = f"(?:{'|'.join(Patterns.getInstance().regexes['space'])})"
WD = Patterns.getInstance().cumulative_annotations['WD']
MNTH = "|".join(const.MILADI_MONTHS.keys())
CJ = Patterns.getInstance().cumulative_annotations['CJ']
time = Patterns.getInstance().regexes['time']

minute_literal = rf"(?P<minute_literal>{ValueExtractor.MIN_LIT})"
hour_literal = rf"(?P<hour_literal>{ValueExtractor.HOUR_LIT})"
day_literal = rf"(?P<day_literal>{'روز'})"
month_literal = rf"(?P<month_literal>{ValueExtractor.MONTH_LIT})"

mh_literals = rf"(?P<mh_literals>{minute_literal}|{hour_literal})"

day = rf"(?P<day>{WD})"

simple_day_range = rf"(?P<from_day>{WD}){space}(?:{CJ}){space}(?P<to_day>{WD})"
day_range = rf"(?P<day_range>{simple_day_range})"
days = rf"(?P<days>{day_range}|{day})"

month = rf"(?P<month>{MNTH})"
month_range = rf"(?P<month_range>(?P<from_month>{MNTH}){space}(?:{CJ}){space}(?P<to_month>{MNTH}))"
months = rf"(?P<months>{month_range}|{month})"

timee = list(map(lambda regex: fr'\b(?:{regex})(?:\b|(?!{const.FA_SYM}|\d+))', time))
time_combined = fr"(?P<time>(" + ")|(".join(timee) + "))"

value = rf"(?P<value>{const.DLARGE})"

pattern1 = rf"{HAR_LITERAL}{space}(?:{value}{space})?{mh_literals}"
pattern2 = rf"{HAR_LITERAL}{space}({days})({space}(?:{time_combined}))?"
pattern3 = rf"{HAR_LITERAL}{space}{time_combined}"
pattern4 = rf"{HAR_LITERAL}{space}(?:{value}{space})?(?:{day_literal})(?:{space}{time_combined})?"
pattern5 = rf"{HAR_LITERAL}{space}(?:{value}{space})?(?:{month_literal})"
pattern6 = rf"{HAR_LITERAL}{space}{months}(?:{space}{days})?(?:{space}?{HA_LITERAL}?)?(?:{space}{time_combined})?"
pattern7 = rf"{days}(?:{space}?{HA_LITERAL})(?:{space}{time_combined})?"

patterns = [eval(f'pattern{i}') for i in range(1, 8)]

fa_wd_to_num = {
    'شنبه': 5,
    'یکشنبه': 6,
    'دوشنبه': 0,
    'دو شنبه': 0,
    'سه‌شنبه': 1,
    'چهارشنبه': 2,
    'پنجشنبه': 3,
    'پنج شنبه': 3,
    'جمعه': 4,
}


def convert_value_to_str(value):
    if value:
        value = const.MINUTES[value]
        value = f"*/{value}"
    else:
        value = '*'
    return value


def convert_match_to_cron(m: re.Match):
    d = m.groupdict()
    vx = ValueExtractor()
    cron = {
        'minute': '*',
        'hour': '*',
        'day': '*',
        'month': '*',
        'weekday': '*',
    }

    if d.get('time', None):
        time = d['time']
        tv = vx.compute_time_value(time)
        tv = tv.split(':')
        hour, minute = int(tv[0]), int(tv[1])
        cron['hour'] = hour
        cron['minute'] = minute
    else:
        cron['minute'] = cron['hour'] = '0'

    if d.get('mh_literals', None):
        value = d.get('value')
        value = convert_value_to_str(value)
        if d.get('minute_literal', None):
            cron['minute'] = value
            cron['hour'] = '*'

        if d.get('hour_literal', None):
            cron['hour'] = value

    if d.get('day_literal', None):
        value = d.get('value')
        value = convert_value_to_str(value)
        cron['day'] = value

    if d.get('days', None):
        if d.get('day', None):
            weekday = fa_wd_to_num[d['day']] + 1
            cron['weekday'] = weekday
        if d.get('day_range', None):
            from_day = d.get('from_day')
            to_day = d.get('to_day')
            assert from_day is not None
            assert to_day is not None
            from_day = fa_wd_to_num[from_day] + 1
            to_day = fa_wd_to_num[to_day] + 1
            if from_day > to_day:
                to_day, from_day = from_day, to_day
            weekdays = f'{from_day}-{to_day}'
            cron['weekday'] = weekdays

    if d.get('month_literal', None):
        value = d.get('value')
        value = convert_value_to_str(value)
        cron['month'] = value
        cron['day'] = '1'

    if d.get('months', None):
        if d.get('month', None):
            single_month = const.MILADI_MONTHS[d['month']]
            cron['month'] = single_month
            cron['day'] = 1

        if d.get('month_range', None):
            from_month = d.get('from_month')
            to_month = d.get('to_month')
            assert from_month is not None
            assert to_month is not None
            from_month = const.MILADI_MONTHS[from_month]
            to_month = const.MILADI_MONTHS[to_month]

            cron['month'] = f'{from_month}-{to_month}'
            cron['day'] = 1

    return f"{cron['minute']} {cron['hour']} {cron['day']} {cron['month']} {cron['weekday']}"


def extract_cron(s):
    for pattern in patterns:
        m = re.search(pattern, s)
        if m:
            cron = convert_match_to_cron(m)
            return cron
    return None


def test_time():
    ve = ValueExtractor()
    z = []
    z.append("ساعت ۵ و پنجاه و هشت دقیقه شب")
    z.append("ساعت ۵ عصر ژانویه")
    z.append("۲۰ دقیقه مانده به شیش عصر")
    z.append("ساعت ۷ و سی ۱ ثانیه")
    z.append("ده صبح")
    z.append("۶:۱۷ صبح")
    z.append("عصر ۶:۱۷")
    z.append("دقیقه ۲۰ تا ۱۷")
    for time in z:
        x = ve.compute_value(time)
        y = ve.compute_time_value(time)
        print(x)
        print(y)


def test_date():
    ve = ValueExtractor()
    z = "دوشنبه تا چهارشنبه پنج فروردین"
    z = "پنج فروردین"
    z = "پنج فروردین سال ۱۴۰۰"
    x = ve.compute_date_value(z)


def verify_day():
    s1 = "دو شنبه"
    m = re.match(day, s1)
    assert m is not None
    s2 = "سه مبه"
    m = re.match(day, s2)
    assert m is None


def verify_simple_day_range():
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
    s1 = ValueExtractor().normalize_numbers(s1)
    m = re.match(time_combined, s1)
    assert m is not None

    s2 = "ساعت ۱۷"

    # s2 = ValueExtractor().normalize_numbers(s2)
    # s3 = "ساعت پنج و پنجاه و هشت دقیقه شب"
    # s2 = s3
    # s2 = ValueExtractor().normalize_numbers(s2)
    # for regex_value in timee:
    #     matches = re.findall(
    #             fr'{regex_value}',
    #             s2)
    #     res = max(matches, default=None)
    #     print(res)

    #     # ignore empty markers
    #     # if len(matches) > 0:
    #     #     print(regex_value)
    #     #     print(matches) 
    #     #     print("found")

    # print(s2)
    m = re.match(time_combined, s2)
    assert m is not None

    s3 = "ساعت پنج و پنجاه و هشت دقیقه شب"
    m = re.match(time_combined, s3)
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
    assert d['mh_literals'] == 'دقیقه'
    assert d['minute_literal'] == 'دقیقه'
    assert d['value'] == None

    s2 = "هر دو ساعت"
    m = re.match(pattern1, s2)
    assert m is not None
    d = m.groupdict()
    assert d['mh_literals'] == 'ساعت'
    assert d['hour_literal'] == 'ساعت'
    assert d['value'] == 'دو'


def verify_pattern2():
    s1 = 'هر پنجشنبه تا جمعه ساعت ۱۷'""
    m = re.match(pattern2, s1)
    assert m is not None

    s2 = "هر دوشنبه"
    m = re.match(pattern2, s2)
    assert m is not None


def verify_pattern3():
    s1 = "هر ساعت شش عصر"
    m = re.match(pattern3, s1)
    assert m is not None


def verify_pattern4():
    s1 = "هر روز"
    m = re.match(pattern4, s1)
    assert m is not None

    s2 = "هر دو روز"
    m = re.match(pattern4, s2)
    assert m is not None

    s3 = "هر سه روز ساعت پنج و پنجاه و هشت دقیقه شب"
    m = re.match(pattern4, s3)
    assert m is not None
    d = m.groupdict()


def verify_patterns():
    verify_pattern1()
    verify_pattern2()
    verify_pattern3()
    verify_pattern4()


if __name__ == "__main__":
    test_time()
    test_date()
    verify_regexes()
    verify_patterns()
    test_time()
