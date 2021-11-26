import re

SHAMSHI_MONTHS = {
    "فروردین": 1,
    "اردیبهشت": 2,
    "خرداد": 3,
    "تیر": 4,
    "مرداد": 5,
    "شهریور": 6,
    "مهر": 7,
    "آبان": 8,
    "ابان": 8,
    "آذر": 9,
    "اذر": 9,
    "دی": 10,
    "بهمن": 11,
    "اسفند": 12
}
GHAMARI_MONTHS = {
    "محرم": 1,
    "صفر": 2,
    "ربیع‌الاول": 3,
    "ربیع الاول": 3,
    "ربیع اول": 3,
    "ربیع‌اول": 3,
    "ریبع‌الاثانی": 4,
    "ربیع الثانی": 4,
    "ربیع الاثانی": 4,
    "جمادی‌الاول": 5,
    "جمادی الاول": 5,
    "جمادی‌الثانی": 6,
    "جمادی الثانی": 6,
    "رجب": 7,
    "شعبان": 8,
    "رمضان": 9,
    "شوال": 10,
    "ذوالقعده": 11,
    "ذو القعده": 11,
    "ذو قعده": 11,
    "ذی‌القعده": 11,
    "ذی القعده": 11,
    "ذی قعده": 11,
    "ذوالحجه": 12,
    "ذو الحجه": 12,
    "ذو‌الحجه": 12,
    "ذی الحجه": 12,
    "ذی حجه": 12,
    "ذی‌الحجه": 12
}

MILADI_MONTHS = {
    "ژانویه": 1,
    "فوریه": 2,
    "فبریه": 2,
    "مارس": 3,
    "مارچ": 3,
    "آوریل": 4,
    "آپریل": 4,
    "اپریل": 4,
    "اوریل": 4,
    "مه": 5,
    "می": 5,
    "ژوئن": 6,
    "ژوین": 6,
    "ژون": 6,
    "ژوییه": 7,
    "ژوئیه": 7,
    "جولای": 7,
    "اوت": 8,
    "آگوست": 8,
    "اگوست": 8,
    "سپتامبر": 9,
    "سپتامر": 9,
    "اکتبر": 10,
    "نوامبر": 11,
    "دسامبر": 12
}

ONES_TEXT = {
    'صفر': 0,
    'یک': 1,
    'یکم': 1,
    'دو': 2,
    'دوم': 2,
    'سه': 3,
    'سوم': 3,
    'چهار': 4,
    'چهارم': 4,
    'پنج': 5,
    'پنجم': 5,
    'شش': 6,
    'ششم': 6,
    'شیش': 6,
    'شیشم': 6,
    'هفت': 7,
    'هفتم': 7,
    'هشت': 8,
    'هشتم': 8,
    'نه': 9,
    'نهم': 9,
    'دهم': 10,
    'ده': 10
}

TENS_TEXT = {
    'بیست': 20,
    'بیستم': 20,
    'سی': 30,
    'چهل': 40,
    'چهلم': 40,
    'پنجاه': 50,
    'پنجاهم': 50,
    'شصت': 60,
    'شصتم': 60,
    'هفتاد': 70,
    'هفتادم': 70,
    'هشتاد': 80,
    'هشتادم': 80,
    'نود': 90,
    'نودم': 90,
}

TEN_PLUS_TEXT = {
    'یازده': 11,
    'یازدهم': 11,
    'دوازده': 12,
    'دوازدهم': 12,
    'سیزده': 13,
    'سیزدهم': 13,
    'چهارده': 14,
    'چهاردهم': 14,
    'پانزده': 15,
    'پانزدهم': 15,
    'شانزده': 16,
    'شانزدهم': 16,
    'هفده': 17,
    'هفدهم': 17,
    'هجده': 18,
    'هجدهم': 18,
    'نوزده': 19,
    'نوزدهم': 19,
}

HUNDREDS_TEXT = {
    'یکصد': 100,
    'صد': 100,
    'دویست': 200,
    'سیصد': 300,
    'چهارصد': 400,
    'پانصد': 500,
    'ششصد': 600,
    'شیشصد': 600,
    'هفتصد': 700,
    'هشتصد': 800,
    'نهصد': 900,
}

MAGNITUDE = {
    'هزار': 1000,
    'میلیون': 1000000,
    'بیلیون': 1000000000,
    'میلیارد': 1000000000,
    'تریلیون': 1000000000000,
}

TYPO_LIST = {
    'سی ام': 'سی',
    'سی‌ام': 'سی',
    'شیش صد': 'ششصد',
    'شش صد': 'ششصد',
    'هفت صد': 'هفتصد',
    'هشت صد': 'هشتصد',
    'نه صد': 'نهصد',
}

FA_TO_EN = {
    '۰': '0',
    '۱': '1',
    '۲': '2',
    '۳': '3',
    '۴': '4',
    '۵': '5',
    '۶': '6',
    '۷': '7',
    '۸': '8',
    '۹': '9'
}


SHAMSI_LIST = '|'.join(list(SHAMSHI_MONTHS.keys()))
GHAMARI_LIST = '|'.join(list(GHAMARI_MONTHS.keys()))
MILADI_LIST = '|'.join(list(MILADI_MONTHS.keys()))
ALL_MONTHS = SHAMSI_LIST + '|' + GHAMARI_LIST + '|' + MILADI_LIST

Units = "|".join(
    list(TEN_PLUS_TEXT.keys()) + list(HUNDREDS_TEXT.keys()) + list(MAGNITUDE.keys()) + list(TENS_TEXT.keys()) + list(
        ONES_TEXT.keys()) + list(TYPO_LIST.keys()))

FA_NUMBERS = "۰|۱|۲|۳|۴|۵|۶|۷|۸|۹"
EN_NUMBERS = "0|1|2|3|4|5|6|7|8|9"
Symbols = ":|/|-"
C_NUMBERS = FA_NUMBERS + "|" + EN_NUMBERS + "|" + Symbols

JOINER = 'و'
MONTH_LIT = 'ماه'
YEAR_LIT = 'سال'
DATE_JOINER = '-|/'

def date_value_extractor(text):
    def normalize_numbers(_text):
        pattern = "|".join(map(re.escape, FA_TO_EN.keys()))
        return re.sub(pattern, lambda m: FA_TO_EN[m.group()], str(_text))

    def normalize_space(_text):
        res_space = re.sub(fr'((?:{C_NUMBERS})+(\.(?:{C_NUMBERS})+)?)', r' \1 ', _text)
        res_space = ' '.join(res_space.split())
        return res_space

    def tokenize(_text):
        for typo in TYPO_LIST.keys():
            if typo in _text:
                _text = _text.replace(typo, TYPO_LIST[typo])
        slitted_text = _text.split(' ')
        slitted_text = [txt for txt in slitted_text if txt != JOINER]

        return slitted_text

    def remove_ordinal_suffix(_text):
        word = _text.replace('مین', '')
        word = word.replace(' ام', '')
        word = word.replace(' اُم', '')

        if word.endswith('سوم'):
            return word[:-3] + 'سه'
        elif word.endswith('م'):
            return word[:-1]
        return word

    def compute(tokens):
        result = 0

        for token in tokens:
            if ONES_TEXT.get(token):
                result += ONES_TEXT[token]
            if TEN_PLUS_TEXT.get(token):
                result += TEN_PLUS_TEXT[token]
            if TENS_TEXT.get(token):
                result += TENS_TEXT[token]
            elif HUNDREDS_TEXT.get(token):
                result += HUNDREDS_TEXT[token]
            elif token.isdigit():
                result += int(token)
            elif MAGNITUDE.get(token):
                result = result * MAGNITUDE[token] if result != 0 else MAGNITUDE[token]

        return result

    def convert_word_to_digits(_text):

        if _text == '' or _text is None or _text == ' ':
            return ' '

        if normalize_space(_text) == JOINER:
            return ' ' + JOINER + ' '

        text_date = remove_ordinal_suffix(_text)
        computed = compute(tokenize(text_date))
        return computed

    def date_reformat(_text):
        try:
            # format number 1
            date_format_num1 = fr'(\d+)\s*[(?:\b{MONTH_LIT})]*\s*(\b{ALL_MONTHS})\s*[(?:\b{MONTH_LIT})]*\s*[(?:\b{YEAR_LIT})]* (\d+)'
            day_month_year = re.search(date_format_num1, _text).groups()

            day = int(day_month_year[0])
            month = day_month_year[1]
            year = int(day_month_year[2])

            if month in MILADI_MONTHS.keys():
                month_index = MILADI_MONTHS[month]
                return f'{day:02}/{month_index:02}/{year}'
            elif month in GHAMARI_MONTHS.keys():
                # TODO : Improve offset 1400:
                # if the shamsi year is lower than 100 then assume it has 13 before it
                if day < 100 and year < 100:
                    year += 1400
                month_index = GHAMARI_MONTHS[month]
                return f'{year}/{month_index:02}/{day:02}ه.ق  '
            elif month in SHAMSHI_MONTHS.keys():
                # TODO : Improve offset 1300:
                # if the shamsi year is lower than 100 then assume it has 13 before it
                if day < 100 and year < 100:
                    year += 1300

                month_index = SHAMSHI_MONTHS[month]
                return f'{year}/{month_index:02}/{day:02}'
            else:
                return f'{year}/{month}/{day:02}'
        except:
            pass

        try:
            # format number 2
            date_format_num2 = fr'(\d+)\s*[(?:\b{DATE_JOINER})]\s*(\d+)\s*[(?:\b{DATE_JOINER})]\s*(\d+)'
            detected_date = re.search(date_format_num2, _text).groups()

            year = int(detected_date[0])
            month = int(detected_date[1])
            day = int(detected_date[2])

            # TODO : Improve these constraints for different days:
            # if year is lower than 100 then assume it has 13 before it
            if day < 100 and year < 100:
                year += 1300
            # assume the greater value as year
            if day > year or 'میلادی' in _text:
                year, day = day, year

            # ghamari
            if 'قمری' in _text:
                return f'{year}/{month:02}/{day:02}ه.ق  '
            # miladi date:
            if year > 1800 or 'میلادی' in _text:
                return f'{day:02}/{month:02}/{year:02}'
            # shamsi date
            else:
                return f'{year:02}/{month:02}/{day:02}'
        except:
            return None

    text = normalize_numbers(text)
    res = re.sub(fr'\b(?:{Units}|\s{JOINER}\s|\s|\d{1, 4})+\b', lambda m: str(convert_word_to_digits(m.group())), text)
    res = normalize_space(res)
    res = date_reformat(res) if date_reformat(res) is not None else res
    res = normalize_space(res)
    return res
