from curses import keyname
from ..marker_extractor import ValueExtractor
from datetime import datetime

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
    return 'و' in text


def get_ts_from_phrase(text: str):
    for fa_word, ts in convertor_fa_2_timestamp.items():
            if fa_word in text:
                return round(datetime.now().timestamp() + ts)


def remove_starting_keyword(text: str):
    for starting_keyword in duration_set_start:
        if text.startswith(starting_keyword):
            text = text.replace(starting_keyword, '')
    return text


def extract_duration_start(span, text: str):
    for keyword in duration_set_start:
        if text.startswith(keyword) and not has_va(text):
            stripped_text = remove_starting_keyword(text)
            return {
                'type': 'duration',
                'text': text,
                'span': span,
                'value':{
                    get_ts_from_phrase('حالا'), vx.compute_value(stripped_text)
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
