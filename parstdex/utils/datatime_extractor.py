from typing import List
from ..marker_extractor import ValueExtractor
from . import const
from datetime import datetime, date, timedelta
import requests
from bs4 import BeautifulSoup
import re

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
    'دوشنبه': 0,
    'سه‌شنبه': 1,
    'چهارشنبه': 2,
    'پنجشنبه': 3,
    'جمعه': 4,
}


def fa_wd_to_duration(wd: str):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    wd_num = fa_wd_to_num[wd]
    delta = (wd_num - today.weekday() + 7) % 7
    delta = 7 if delta == 0 else delta
    target_day = today.day + delta
    target_ts = int(today.replace(day=target_day).timestamp())
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

def get_ghamari_mnth_duration(text: str) -> int:
    year, month, day = get_current_ghamari()

    month_number = const.GHAMARI_MONTHS[text]
    year_number = year + 1 if month_number < month else year

    next_month = 1 if month_number == 12 else (month_number + 1)
    next_year = year_number + 1 if month_number == 12 else year_number

    begin_ts = int(convert_ghamari_to_miladi(year_number, month_number, 1).timestamp())
    end_ts = int(convert_ghamari_to_miladi(next_year, next_month, 1).timestamp())

    return [begin_ts, end_ts]

def get_shamsi_mnth_duration(text: str):
    year, month, day = get_current_shamsi()

    month_number = const.SHAMSHI_MONTHS[text]
    year_number = year + 1 if month_number < month else year

    next_month = 1 if month_number == 12 else (month_number + 1)
    next_year = year_number + 1 if month_number == 12 else year_number

    begin_ts = int(convert_shamsi_to_miladi(year_number, month_number, 1).timestamp())
    end_ts = int(convert_shamsi_to_miladi(next_year, next_month, 1).timestamp())

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
}


def extract_duration_start(span, text: str):
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
            elif re.search(const.ONE_NINETY_NINE_JOIN, stripped_text) is not None:
                number = re.search(const.ONE_NINETY_NINE_JOIN, stripped_text).group(0)
                stripped_text = stripped_text.replace(number, '').strip()
                number = const.ONE_NINETY_NINE[number]
                current_ts = int(datetime.now().timestamp())
                value = [current_ts, current_ts + number * time_length[stripped_text]]
            elif re.search(r'\d+', vx.compute_value(stripped_text)) is not None:
                computed_value = vx.compute_value(stripped_text)
                number = re.search(r'\d+', computed_value).group(0)
                computed_value = computed_value.replace(number, '').strip()
                number = int(number)
                current_ts = int(datetime.now().timestamp())
                value = [current_ts, current_ts + number * time_length[computed_value]]

            elif re.search(r'\d+(\\|\/)\d+(\\|\/)\d+', stripped_text) is not None:
                match = re.search(r'(\d+)(\\|\/)(\d+)(\\|\/)(\d+)', stripped_text)
                if 'ه.ش' in stripped_text or 'شمسی' in stripped_text or 'خورشیدی' in stripped_text:
                    value = [int(convert_shamsi_to_miladi(match.group(1), match.group(3), match.group(5)).timestamp())]
                elif 'ه.ق' in stripped_text or 'قمری' in stripped_text:
                    value = [int(convert_ghamari_to_miladi(match.group(1), match.group(3), match.group(5)).timestamp())]
                elif 'میلادی' in stripped_text or '.م' in stripped_text:
                    value = [int(datetime(match.group(1), match.group(3), match.group(5), 0, 0, 0, 0).timestamp())]

            else:
                value = [get_ts_from_phrase('حالا'), vx.compute_value(stripped_text)]

            return {
                'type': 'duration',
                'text': text,
                'span': span,
                'value':{
                    value[0], value[1]
                }
            }


def extract_duration_middle(span, text: str):
    for keyword in duration_set_middle:
        if keyword in text:
            stripped_text = remove_starting_keyword(text)
            tmp = stripped_text.split(keyword)

            if tmp[0].strip() == '':
                tmp[0] = 'حالا'

            begin = get_ts_from_phrase(tmp[0])
            end = get_ts_from_phrase(tmp[1])

            return {
                'type': 'duration',
                'text': text,
                'span': span,
                'value':{
                    begin, end
                }
            }


def extract_duration(markers: dict):
    res = []
    for k, v in markers['datetime'].items():
        if is_duration(v): # redundant
            if has_middle_keyword(v):
                res.append(extract_duration_middle(k, v))
            else:
                res.append(extract_duration_start(k, v))
    return res
