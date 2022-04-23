from ..marker_extractor import ValueExtractor
from datetime import datetime

duration_set = {
    'تا',
    'لغایت',
    'الی',
    'طی',
    'الی',
    'در بازه',
    'ظرف',
    'در مدت',
    'طی مدت',
    'طول',
    'بازه',
    'حد فاصل',
    'در عرض',
    'بین',
}

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
    'دیروز': -1 * 24 * 60 * 60,
    'دیشب': -1 * 24 * 60 * 60,
    'پریروز': -2 * 24 * 60 * 60,
    'پریشب': -2 * 24 * 60 * 60,

}

vx = ValueExtractor()

def get_ts_from_phrase(text: str):
    for fa_word, ts in convertor_fa_2_timestamp.items():
            if fa_word in text:
                return round(datetime.now().timestamp() + ts)


def extract_duration(markers: dict, values: dict):
    res = []
    for keyword in duration_set:
        # print(list(markers.keys), list(markers.values))
        print(markers)
        for k, v in markers['datetime'].items():
            if keyword in v:
                tmp = v.split(keyword)
                begin = get_ts_from_phrase(tmp[0])
                end = get_ts_from_phrase(tmp[1])

                res.append({
                    'type': 'duration',
                    'text': v,
                    'span': k,
                    'value':{
                        begin, end
                    }
                })

    return res
