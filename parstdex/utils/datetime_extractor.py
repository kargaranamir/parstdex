from typing import List
from ..marker_extractor import ValueExtractor
from . import const
from datetime import datetime, date, timedelta
import requests
from bs4 import BeautifulSoup
import re
import calendar

duration_set_middle = {
    'تا',
    'لغایت',
    'الی',
}

duration_set_start = {
    'طی',
    'در بازه',
    'ظرف',
    'در مدت',
    'طی مدت',
    'طول',
    'بازه',
    'حد فاصل',
    'در عرض',
    'بین',
    'از',
    'در فاصله',
}

duration_set = duration_set_middle.union(duration_set_start)

cron_set = {
    'ها',
    'هر',
    'های',
}

convertor_fa_2_timestamp = {
    'فردا': 24 * 60 * 60,
    'پسفردا': 2 * 24 * 60 * 60,
    'پس‌فردا': 2 * 24 * 60 * 60,
    'امروز': 0,
    'حال': 0,
    'به حال': 0,
    'بکنون': 0,
    'به کنون': 0,
    'اکنون': 0,
    'حالا': 0,
    'کنون': 0,
    'دیروز': -1 * 24 * 60 * 60,
    'دیشب': -1 * 24 * 60 * 60,
    'پریروز': -2 * 24 * 60 * 60,
    'پریشب': -2 * 24 * 60 * 60,

}

prior = ['گذشته', 'قبل', 'قبلی', 'ماضی', 'پیش', 'پیشین']
future = ['دیگر', 'بعد', 'آتی']

vx = ValueExtractor()


def is_duration(text: str) -> bool:
    return any(keyword in text for keyword in duration_set)


def has_middle_keyword(text: str) -> bool:
    return any(keyword in text for keyword in duration_set_middle)


def has_va(text: str) -> bool:
    return ' و ' in text


def get_ts_from_phrase(text: str):
    for fa_word, ts in convertor_fa_2_timestamp.items():
            if fa_word in text:
                return round(datetime.now().timestamp() + ts)


fa_wd_to_num = {
    'شنبه': 5,
    'یکشنبه': 6,
    'یک شنبه': 6,
    'یک‌شنبه': 6,
    'دوشنبه': 0,
    'دو‌شنبه': 0,
    'سه‌شنبه': 1,
    'سشنبه': 1,
    'سه‌ شنبه': 1,
    'چهارشنبه': 2,
    'چهار‌شنبه': 2,
    'چهار شنبه': 2,
    'پنجشنبه': 3,
    'پنج‌شنبه': 3,
    'پنج شنبه': 3,
    'جمعه': 4,
}


def fa_wd_to_duration(wd: str):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    wd_num = fa_wd_to_num[wd]
    delta = (wd_num - today.weekday() + 7) % 7
    delta = 7 if delta == 0 else delta
    target_ts = int(today.timestamp()) + delta * 24 * 60 * 60
    return [target_ts, target_ts + 24 * 60 * 60]


def miladi_mnth_to_duration(mnth: str) -> int:
    year = datetime.now().year
    month = const.MILADI_MONTHS[mnth]
    next_month = month + 1 if month < 12 else 1
    begin_timestamp = int(datetime(year=year, month=month, day=1).timestamp())
    end_timestamp = int(datetime(year=year, month=next_month, day=1).timestamp())
    return [begin_timestamp, end_timestamp]


def get_current_shamsi() -> List[int]:
    now = datetime.now()
    URL = 'https://www.time.ir/'
    PARAMS = {
        'convertyear': now.year,
        'convertmonth': now.month,
        'convertday': now.day,
        'convertlcid': 1033,
        '_': datetime.timestamp(now),
    }
    resp = requests.get(URL, params=PARAMS)
    soup = BeautifulSoup(resp.content, 'html.parser')
    d = soup.find('span', id='ctl00_cphMiddle_Sampa_Web_View_TimeUI_DateConvert00cphMiddle_3733_lblSecondDateNumeral')
    year, month, day = d.text.split('/')
    for fa, en in const.FA_TO_EN.items():
        year = year.replace(fa, en)
        month = month.replace(fa, en)
        day = day.replace(fa, en)
    return int(year), int(month), int(day)

def get_current_ghamari() -> List[int]:
    now = datetime.now()
    URL = 'https://www.time.ir/'
    PARAMS = {
        'convertyear': now.year,
        'convertmonth': now.month,
        'convertday': now.day,
        'convertlcid': 1033,
        '_': datetime.timestamp(now),
    }
    resp = requests.get(URL, params=PARAMS)
    soup = BeautifulSoup(resp.content, 'html.parser')
    d = soup.find('span', id='ctl00_cphMiddle_Sampa_Web_View_TimeUI_DateConvert00cphMiddle_3733_lblThirdDateNumeral')
    year, month, day = d.text.split('/')
    for fa, en in const.FA_TO_EN.items():
        year = year.replace(fa, en)
        month = month.replace(fa, en)
        day = day.replace(fa, en)
    return int(year), int(month), int(day)

def convert_ghamari_to_miladi(year, month, day) -> datetime:
    URL = 'https://www.time.ir/'
    PARAMS = {
        'convertyear': year,
        'convertmonth': month,
        'convertday': day,
        'convertlcid': 1025,
        '_': datetime.now().timestamp(),
    }
    resp = requests.get(URL, params=PARAMS)
    soup = BeautifulSoup(resp.content, 'html.parser')
    d = soup.find('span', id='ctl00_cphMiddle_Sampa_Web_View_TimeUI_DateConvert00cphMiddle_3733_lblThirdDateNumeral')
    year, month, day = d.text.split('-')
    year, month, day = int(year), int(month), int(day)
    return datetime(year, month, day)



def convert_shamsi_to_miladi(year, month, day) -> datetime:
    URL = 'https://www.time.ir/'
    PARAMS = {
        'convertyear': year,
        'convertmonth': month,
        'convertday': day,
        'convertlcid': 1065,
        '_': 0,
    }
    resp = requests.get(URL, params=PARAMS)
    soup = BeautifulSoup(resp.content, 'html.parser')
    d = soup.find('span', id='ctl00_cphMiddle_Sampa_Web_View_TimeUI_DateConvert00cphMiddle_3733_lblSecondDateNumeral')
    year, month, day = d.text.split('-')
    year, month, day = int(year), int(month), int(day)
    return datetime(year, month, day)

def get_ghamari_mnth_duration(month_text: str, day : int = 1) -> int:
    year, month, day = get_current_ghamari()

    month_number = const.GHAMARI_MONTHS[month_text]
    year_number = year + 1 if month_number < month else year

    next_month = 1 if month_number == 12 else (month_number + 1)
    next_year = year_number + 1 if month_number == 12 else year_number

    begin_ts = int(convert_ghamari_to_miladi(year_number, month_number, day).timestamp())
    end_ts = int(convert_ghamari_to_miladi(next_year, next_month, day).timestamp())

    return [begin_ts, end_ts]

def get_miladi_mnth_duration(month_text: str, day : int = 1):
    year, month, day = datetime.now().year, datetime.now().month, datetime.now().day

    month_number = const.MILADI_MONTHS[month_text]
    year_number = year + 1 if month_number < month else year

    next_month = 1 if month_number == 12 else (month_number + 1)
    next_year = year_number + 1 if month_number == 12 else year_number

    begin_ts = int(datetime(year_number, month_number, day).timestamp())
    end_ts = int(datetime(next_year, next_month, day).timestamp())

    return [begin_ts, end_ts]


def get_shamsi_mnth_duration(month_text: str, day : int = 1):
    year, month, day = get_current_shamsi()

    month_number = const.SHAMSHI_MONTHS[month_text]
    year_number = year + 1 if month_number < month else year

    next_month = 1 if month_number == 12 else (month_number + 1)
    next_year = year_number + 1 if month_number == 12 else year_number

    begin_ts = int(convert_shamsi_to_miladi(year_number, month_number, day).timestamp())
    end_ts = int(convert_shamsi_to_miladi(next_year, next_month, day).timestamp())

    return [begin_ts, end_ts]

def remove_starting_keyword(text: str):
    for starting_keyword in duration_set_start:
        if text.startswith(starting_keyword):
            text = text.replace(starting_keyword, '')
    return text


time_length = {
    'ثانیه': 1,
    'دقیقه': 60,
    'ساعت': 60 * 60,
    'روز': 24 * 60 * 60,
    'هفته': 7 * 24 * 60 * 60,
    'ماه': 30 * 24 * 60 * 60,
    'ماهه': 30 * 24 * 60 * 60,
    'سال': 12 * 30 * 24 * 60 * 60,
    'هزاره': 1000 * 12 * 30 * 24 * 60 * 60,
}

def is_year_month_day(text: str):
    return re.search(r'\d+(\\|\/)\d+(\\|\/)\d+', text) is not None

def extract_year_month_day(text: str):
    """
    12/123/12 ه.ق
    ۱۲\۱۲\۱۲ میلادی
    """
    match = re.search(r'(\d+)(\\|\/)(\d+)(\\|\/)(\d+)', text)
    if 'ه.ش' in text or 'شمسی' in text or 'خورشیدی' in text:
        return int(convert_shamsi_to_miladi(int(match.group(1)), int(match.group(3)), int(match.group(5))).timestamp())
    elif 'ه.ق' in text or 'قمری' in text:
        return int(convert_ghamari_to_miladi(int(match.group(1)), int(match.group(3)), int(match.group(5))).timestamp())
    elif 'میلادی' in text or '.م' in text:
        return int(datetime(int(match.group(1)), int(match.group(3)), int(match.group(5)), 0, 0, 0, 0).timestamp())
    else:
        return int(convert_shamsi_to_miladi(int(match.group(1)), int(match.group(3)), int(match.group(5))).timestamp())


def contains_text_number(text: str) -> bool:
    """
    دو روز
    دو سال
    دو ماه
    """
    for x in const.ONE_NINETY_NINE.keys():
        if x in text.split():
            return True

    return False

def extract_text_number_duration(text: str):
    """
    طی دو ماه
    """
    text = remove_redundants(text)
    number = re.search(const.ONE_NINETY_NINE_JOIN, text).group(0)
    text = text.replace(number, '').strip()
    number = const.ONE_NINETY_NINE[number]
    current_ts = int(datetime.now().timestamp())
    sign = 1
    for p in prior:
        if p in text:
            sign = -1
            text = text.replace(p, '').strip()
            break

    if sign == 1:
        return [current_ts, current_ts +  number * time_length[text]]
    else:
        return [ current_ts + -1 * number * time_length[text], current_ts]


def contains_number(text: str) -> bool:
    """
    در عرض ۱ ثانیه
    """
    return re.search(r'\d+', vx.compute_value(text)) is not None and any(tl in text for tl in time_length.keys())


def extract_number_duration(text: str):
    text = remove_redundants(text)
    computed_value = vx.compute_value(text)
    number = re.search(r'\d+', computed_value).group(0)
    computed_value = computed_value.replace(number, '').strip()
    number = int(number)
    current_ts = int(datetime.now().timestamp())
    sign = 1
    for p in prior:
        if p in computed_value:
            sign = -1
            computed_value = computed_value.replace(p, '').strip()
            break
    if sign == 1:
        return [current_ts, current_ts + number * time_length[computed_value]]
    else:
        return [current_ts + -1 * number * time_length[computed_value], current_ts]


def extract_wd(text: str):
    weekday = None
    for wd in fa_wd_to_num.keys():
        if wd in text.split():
            start, end = fa_wd_to_duration(wd)
            weekday = wd
            text = text.replace(wd, '')
            break
    else:
        return False

    number = 1
    if contains_text_number(text):
        number = const.ONE_NINETY_NINE[re.search(const.ONE_NINETY_NINE_JOIN, text).group(0)]
    elif contains_number(text):
        number = int(re.search(r'\d+', vx.compute_value(text)).group(0))

    period = 0
    if 'هفته' in text:
        period = time_length['هفته']

    sign = 1
    for p in prior:
        if p in text:
            sign = -1
            period = time_length['هفته']
            text = text.replace(p, '').strip()
            break

    return start + sign * number * period, end + sign * number * period


def is_simple_duration(text: str):
    text = text.split()
    if len(text) != 2:
        return False
    if text[0] in time_length and (text[1] in prior or text[1] in future):
        return True
    return False


def extract_duration_only(text: str):
    """
    روز بعد
    هفته قبل
    سال پیش
    """
    for p in prior:
        if p in text:
            sign = -1
            text = text.replace(p, '').strip()
    for f in future:
        if f in text:
            sign = 1
            text = text.replace(p, '').strip()
    period = time_length[text]
    now = int(datetime.now().timestamp())
    if sign < 0:
        return now - period, now
    else:
        return now, now + period

def extract_duration_start(text: str):
    for keyword in duration_set_start:
        if text.startswith(keyword) and not has_va(text):
            stripped_text = remove_starting_keyword(text)
            stripped_text = stripped_text.strip()

            if stripped_text in fa_wd_to_num:
                value = fa_wd_to_duration(stripped_text)
            elif stripped_text in const.MILADI_MONTHS:
                value = miladi_mnth_to_duration(stripped_text)
            elif stripped_text in const.GHAMARI_MONTHS:
                value = get_ghamari_mnth_duration(stripped_text)
            elif stripped_text in const.SHAMSHI_MONTHS:
                value = get_shamsi_mnth_duration(stripped_text)
            elif contains_text_number(stripped_text):
                value = extract_text_number_duration(stripped_text)
            elif contains_number(stripped_text):
                value = extract_number_duration(stripped_text)
            elif is_year_month_day(stripped_text):
                value = extract_year_month_day(stripped_text)
            elif is_simple_duration(stripped_text):
                value = extract_duration_only(stripped_text)
            else:
                value = [get_ts_from_phrase('حالا'), vx.compute_value(stripped_text)]

            return value


def is_month_day(text):
    if any(shamsi_month in text for shamsi_month in const.SHAMSHI_MONTHS.keys()) and \
        bool(re.search(r'\d+', text)):
        return True

    return False

def extract_month_day(text):
    day = int(re.search('\d+', text).group())
    for shamsi_month in const.SHAMSHI_MONTHS.keys():
        if shamsi_month in text:
            return get_shamsi_mnth_duration(month_text=shamsi_month, day=day)
    for ghamari_month in const.GHAMARI_MONTHS.keys():
        if ghamari_month in text:
            return get_ghamari_mnth_duration(month_text=ghamari_month, day=day)
    for miladi_month in const.MILADI_MONTHS.keys():
        if miladi_month in text:
            return get_miladi_mnth_duration(month_text=miladi_month, day=day)


def extract_duration_middle(text: str):
    for keyword in duration_set_middle:
        if keyword in text:
            stripped_text = remove_starting_keyword(text)
            tmp = stripped_text.split(keyword)

            if tmp[0] == '':
                tmp[0] = 'حالا'

            value = [None, None]

            for i in range(2):
                text = tmp[i]
                val = get_ts_from_phrase(text)
                if val is None:
                    if extract_wd(text):
                        val = extract_wd(text)[i]
                    elif text in const.MILADI_MONTHS:
                        val = miladi_mnth_to_duration(text)[i]
                    elif text in const.GHAMARI_MONTHS:
                        val = get_ghamari_mnth_duration(text)[i]
                    elif text in const.SHAMSHI_MONTHS:
                        val = get_shamsi_mnth_duration(text)[i]
                    elif contains_text_number(text):
                        val = extract_text_number_duration(text)[i]
                    elif contains_number(text):
                        val = extract_number_duration(text)[i]
                    elif is_year_month_day(text):
                        val = extract_year_month_day(text)
                    elif is_simple_duration(text):
                        value = extract_duration_only(text)[i]
                    elif is_month_day(text):
                        val = extract_month_day(text)[i]
                    else:
                        val = vx.compute_value(text)
                value[i] = val

            return value


def remove_redundants(text: str):
    for p in future:
        text = text.replace(p, '')
    return text

def extract_duration(s: str):
    if has_middle_keyword(s):
        res = extract_duration_middle(s)
    else:
        res = extract_duration_start(s)
    return res


def is_crontime(text: str):
    split_text = re.split(' |‌', text)
    return any(cron_word in split_text for cron_word in cron_set)


def extract_exact_datetime(text: str):
    stripped_text = text.strip()
    computed_value = vx.compute_value(stripped_text)

    value = get_ts_from_phrase(computed_value)
    if value is None:
        if extract_wd(stripped_text):
            value = extract_wd(stripped_text)[0]
        elif stripped_text in const.MILADI_MONTHS:
            value = miladi_mnth_to_duration(stripped_text)[0]
        elif stripped_text in const.GHAMARI_MONTHS:
            value = get_ghamari_mnth_duration(stripped_text)[0]
        elif stripped_text in const.SHAMSHI_MONTHS:
            value = get_shamsi_mnth_duration(stripped_text)[0]
        elif is_year_month_day(stripped_text):
            value = extract_year_month_day(stripped_text)
        elif is_simple_duration(stripped_text):
            value = extract_duration_only(stripped_text)[0]
        elif extract_wd(computed_value):
            value = extract_wd(computed_value)[0]
        elif computed_value in const.MILADI_MONTHS:
            value = miladi_mnth_to_duration(computed_value)[0]
        elif computed_value in const.GHAMARI_MONTHS:
            value = get_ghamari_mnth_duration(computed_value)[0]
        elif computed_value in const.SHAMSHI_MONTHS:
            value = get_shamsi_mnth_duration(computed_value)[0]
        elif is_year_month_day(computed_value):
            value = extract_year_month_day(computed_value)
        elif is_simple_duration(computed_value):
            value = extract_duration_only(computed_value)[0]
        elif is_month_day(computed_value):
            value = extract_month_day(computed_value)[0]
        else:
            value = ''

    return value


def extract_exact_or_duration(markers: dict):
    res = []
    for k, v in markers['datetime'].items():
        if not is_duration(v) and not is_crontime(v):
            res.append(extract_exact_datetime(k, v))
        elif is_duration(v):
            if has_middle_keyword(v):
                res.append(extract_duration_middle(k, v))
            else:
                res.append(extract_duration_start(k, v))
    return res
