import re


class ValueExtractor:
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
        "ذی‌الحجه ": 12
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

    MINUTES = {
        "صفر": 0,
        "یک": 1,
        "دو": 2,
        "سه": 3,
        "چهار": 4,
        "پنج": 5,
        "شش": 6,
        "شیش": 6,
        "هفت": 7,
        "هشت": 8,
        "نه": 9,
        "\bده\b": 10,
        "یازده": 11,
        "دوازده": 12,
        "سیزده": 13,
        "سینزده": 13,
        "چهارده": 14,
        "چارده": 14,
        "پانزده": 15,
        "پونزده": 15,
        "شانزده": 16,
        "شونزده": 16,
        "هفده": 17,
        "هیفده": 17,
        "هجده": 18,
        "هیجده": 18,
        "نونزده": 19,
        "نوزده": 19,
        "بیست": 20,
        "بیست یک": 21,
        "بیست و یک": 21,
        "بیست دو": 22,
        "بیست و دو": 22,
        "بیست سه": 23,
        "بیست و سه": 23,
        "بیست چار": 24,
        "بیست چهار": 24,
        "بیست و چهار": 24,
        "بیست و چار": 24,
        "بیست پنچ": 25,
        "بیست و پنج": 26,
        "بیست شش": 26,
        "بیست و شش": 26,
        "بیست و شیش": 26,
        "بیست هفت": 27,
        "بیست و هفت": 27,
        "بیست هشت": 28,
        "بیست و هشت": 28,
        "بیست و نه": 29,
        "بیست نه": 29,
        "سی": 30,
        "سی یک": 31,
        "سی و یک": 31,
        "سی دو": 32,
        "سی و دو": 32,
        "سی سه": 33,
        "سی و سه": 33,
        "سی چهار": 34,
        "سی چار": 34,
        "سی و چهار": 34,
        "سی و چار": 34,
        "سی پنج": 35,
        "سی و پنج": 35,
        "سی شش": 36,
        "سی شیش": 36,
        "سی و شش": 36,
        "سی و شیش": 36,
        "سی هفت": 37,
        "سی و هفت": 37,
        "سی هشت": 38,
        "سی و هشت": 38,
        "سی نه": 39,
        "سی و نه": 39,
        "چهل": 40,
        "چهل یک": 41,
        "چهل و یک": 41,
        "چهل دو": 42,
        "چهل و دو": 42,
        "چهل سه": 43,
        "چهل و سه": 43,
        "چهل چهار": 44,
        "چهل چار": 44,
        "چهل و چهار": 44,
        "چهل و چار": 44,
        "چهل پنج": 45,
        "چهل و پنج": 45,
        "چهل شش": 46,
        "چهل شیش": 46,
        "چهل و شش": 46,
        "چهل و شیش": 46,
        "چهل هفت": 47,
        "چهل و هفت": 47,
        "چهل هشت": 48,
        "چهل و هشت": 48,
        "چهل نه": 49,
        "چهل و نه": 49,
        "پنجاه": 50,
        "پنجا": 50,
        "پنجاه یک": 51,
        "پنجاه و یک": 51,
        "پنجا و یک": 51,
        "پنجاه دو": 52,
        "پنجاه و دو": 52,
        "پنجا و دو": 52,
        "پنجاه سه": 53,
        "پنجاه و سه": 53,
        "پنجا و سه": 53,
        "پنجاه چهار": 54,
        "پنجاه چار": 54,
        "پنجاه و چهار": 54,
        "پنجاه و چار": 54,
        "پنجا و چهار": 54,
        "پنجا و چار": 54,
        "پنجاه پنج": 55,
        "پنجاه و پنج": 55,
        "پنجا و پنج": 55,
        "پنجاه شش": 56,
        "پنجاه شیش": 56,
        "پنجاه و شش": 56,
        "پنجاه و شیش": 56,
        "پنجا و شش": 56,
        "پنجا و شیش": 56,
        "پنجاه هفت": 57,
        "پنجاه و هفت": 57,
        "پنجا و هفت": 57,
        "پنجاه هشت": 58,
        "پنجاه و هشت": 58,
        "پنجا و هشت": 58,
        "پنجاه و نه": 59,
        "پنجا و نه": 59,
        "پنجاه نه": 59
    }

    HOUR_PART = {
        "ربع": 15,
        "نیم": 30
    }

    DURATION_JOIN = "|".join(
        ["به", "مانده به"]
    )

    SHAMSI_LIST = '|'.join(list(SHAMSHI_MONTHS.keys()))
    GHAMARI_LIST = '|'.join(list(GHAMARI_MONTHS.keys()))
    MILADI_LIST = '|'.join(list(MILADI_MONTHS.keys()))
    ALL_MONTHS = SHAMSI_LIST + '|' + GHAMARI_LIST + '|' + MILADI_LIST
    MINUTES_LIST = '|'.join(list(MINUTES.keys())[::-1])

    FA_NUMBERS = "۰|۱|۲|۳|۴|۵|۶|۷|۸|۹"
    EN_NUMBERS = "0|1|2|3|4|5|6|7|8|9"
    Symbols = ":|/|-"
    C_NUMBERS = FA_NUMBERS + "|" + EN_NUMBERS + "|" + Symbols
    MONTH_LIT = 'ماه'
    YEAR_LIT = 'سال'
    HOUR_LIT = 'ساعت'
    MIN_LIT = 'دقیقه'
    SEC_LIT = 'ثانیه'
    DATE_JOINER = '-|/'
    TIME_JOINER = ':'

    JOINER = 'و'

    Date_Units = "|".join(
        list(TEN_PLUS_TEXT.keys()) + list(HUNDREDS_TEXT.keys()) + list(MAGNITUDE.keys()) + list(
            TENS_TEXT.keys()) + list(
            ONES_TEXT.keys()) + list(TYPO_LIST.keys()))

    ONES_LIST = "|".join(list(ONES_TEXT.keys()))
    TEN_PLUS_LIST = "|".join(list(TEN_PLUS_TEXT))
    TENS_LIST = "|".join(list(TENS_TEXT.keys()))

    def normalize_numbers(self, text):
        pattern = "|".join(map(re.escape, self.FA_TO_EN.keys()))
        return re.sub(pattern, lambda m: self.FA_TO_EN[m.group()], str(text))

    def normalize_space(self, text):
        res_space = re.sub(fr'((?:{self.C_NUMBERS})+(\.(?:{self.C_NUMBERS})+)?)', r' \1 ', text)
        res_space = ' '.join(res_space.split())
        return res_space

    def tokenize(self, text):
        for typo in self.TYPO_LIST.keys():
            if typo in text:
                text = text.replace(typo, self.TYPO_LIST[typo])
        slitted_text = text.split(' ')
        slitted_text = [txt for txt in slitted_text if txt != self.JOINER]

        return slitted_text

    @staticmethod
    def remove_ordinal_suffix(text):
        word = text.replace('مین', '')
        word = word.replace(' ام', '')
        word = word.replace(' اُم', '')

        if word.endswith('سوم'):
            return word[:-3] + 'سه'
        elif word.endswith('م'):
            return word[:-1]
        return word

    def compute_date(self, tokens):
        result = 0

        for token in tokens:
            if self.ONES_TEXT.get(token):
                result += self.ONES_TEXT[token]
            if self.TEN_PLUS_TEXT.get(token):
                result += self.TEN_PLUS_TEXT[token]
            if self.TENS_TEXT.get(token):
                result += self.TENS_TEXT[token]
            elif self.HUNDREDS_TEXT.get(token):
                result += self.HUNDREDS_TEXT[token]
            elif token.isdigit():
                result += int(token)
            elif self.MAGNITUDE.get(token):
                result = result * self.MAGNITUDE[token] if result != 0 else self.MAGNITUDE[token]

        return result

    def convert_word_to_digits(self, text):

        if text == '' or text is None or text == ' ':
            return ' '

        if self.normalize_space(text) == self.JOINER:
            return ' ' + self.JOINER + ' '

        text_date = self.remove_ordinal_suffix(text)
        computed = self.compute_date(self.tokenize(text_date))
        return computed

    def date_reformat(self, text):
        try:
            # format number 1
            date_format_num1 = fr'(\d+)\s*[(?:\b{self.MONTH_LIT})]*\s*(\b{self.ALL_MONTHS})\s*[(?:\b{self.MONTH_LIT})]*\s*[(?:\b{self.YEAR_LIT})]* (\d+)'
            day_month_year = re.search(date_format_num1, text).groups()

            day = int(day_month_year[0])
            month = day_month_year[1]
            year = int(day_month_year[2])

            if month in self.MILADI_MONTHS.keys():
                month_index = self.MILADI_MONTHS[month]
                return f'{day:02}/{month_index:02}/{year}'
            elif month in self.GHAMARI_MONTHS.keys():
                # TODO : Improve offset 1400:
                # if the shamsi year is lower than 100 then assume it has 13 before it
                if day < 100 and year < 100:
                    year += 1400
                month_index = self.GHAMARI_MONTHS[month]
                return f'{year}/{month_index:02}/{day:02}ه.ق  '
            elif month in self.SHAMSHI_MONTHS.keys():
                # TODO : Improve offset 1300:
                # if the shamsi year is lower than 100 then assume it has 13 before it
                if day < 100 and year < 100:
                    year += 1300

                month_index = self.SHAMSHI_MONTHS[month]
                return f'{year}/{month_index:02}/{day:02}'
            else:
                return f'{year}/{month}/{day:02}'
        except:
            pass

        try:
            # format number 2
            date_format_num2 = fr'(\d+)\s*[(?:\b{self.DATE_JOINER})]\s*(\d+)\s*[(?:\b{self.DATE_JOINER})]\s*(\d+)'
            detected_date = re.search(date_format_num2, text).groups()

            year = int(detected_date[0])
            month = int(detected_date[1])
            day = int(detected_date[2])

            # TODO : Improve these constraints for different days:
            # if year is lower than 100 then assume it has 13 before it
            if day < 100 and year < 100:
                year += 1300
            # assume the greater value as year
            if day > year or 'میلادی' in text:
                year, day = day, year

            # ghamari
            if 'قمری' in text:
                return f'{year}/{month:02}/{day:02}ه.ق  '
            # miladi date:
            if year > 1800 or 'میلادی' in text:
                return f'{day:02}/{month:02}/{year:02}'
            # shamsi date
            else:
                return f'{year:02}/{month:02}/{day:02}'
        except:
            return None

    def time_reformat(self, text):
        # ساعت 00:13:42
        try:
            # TODO: ساعت 9:54 ساعت ۰۹:۲۳
            reg = fr'(?:{self.HOUR_LIT})?\s*(\d+)(?:[{self.TIME_JOINER}])(\d*)\s*(?:[{self.TIME_JOINER}])?(\d*)?'

            detected_time = re.search(reg, text).groups()
            hour = int(detected_time[0])
            minute = int(detected_time[1])
            second = int(detected_time[2] if detected_time[2] != '' else "0")
            return f'{hour:02}:{minute:02}:{second:02}'
        except:
            pass

        # ساعت بیست و یک و چهل و دو دقیقه و سی و دو ثانیه
        try:
            reg = fr'(?:{self.HOUR_LIT})\s+(\d+)\s*[{self.JOINER}]?\s*(\d*)\s*(?:{self.MIN_LIT})?\s*[{self.JOINER}]?\s*(\d*)\s*(?:{self.SEC_LIT})?'
            detected_time = re.search(reg, text).groups()
            hour = int(detected_time[0])
            minute = int(detected_time[1] if detected_time[1] != '' else "0")
            second = int(detected_time[2] if detected_time[2] != '' else "0")
            return f'{hour:02}:{minute:02}:{second:02}'
        except:
            pass

        # ساعت 23 دقیقه و 40 ثانیه
        try:
            reg = fr'(?:{self.HOUR_LIT})\s+(\d+)\s*(?:{self.MIN_LIT})\s*[{self.JOINER}]?\s*(\d*)\s*(?:{self.SEC_LIT})?'
            detected_time = re.search(reg, text).groups()
            hour = 0
            minute = int(detected_time[0])
            second = int(detected_time[1])
            return f'{hour:02}:{minute:02}:{second:02}'
        except:
            pass

        try:
            reg = fr'(\d*)\s*[({self.HOUR_LIT})|({self.MIN_LIT})|({self.SEC_LIT})]'
            detected_time = re.search(reg, text).groups()
            hour = 0
            minute = int(detected_time[0])
            second = int(detected_time[1])
            return f'{hour:02}:{minute:02}:{second:02}'
        except:
            pass

    def compute_date_value(self, text):
        text = self.normalize_numbers(text)
        res = re.sub(fr'\b(?:{self.Date_Units}|\s{self.JOINER}\s|\s|\d{1, 4})+\b',
                     lambda m: str(self.convert_word_to_digits(m.group())), text)
        # 23هزار -> 23 هزار
        res = self.normalize_space(res)
        res = self.date_reformat(res) if self.date_reformat(res) is not None else res
        res = self.normalize_space(res)
        return res

    def compute_time_value(self, text):
        text = self.normalize_numbers(text)
        # ساعت بیست و سه و سی چهار دقیقه و چهل و دو ثانیه
        # ساعت بیست و سه - سی و چهار دقیقه - چهل و دو ثانیه
        # یه ربع به یازده
        # بیست و دو دقیقه به ساعت یازده
        # بیست و سه دقیقه و چهل و سه ثانیه مانده به ساعت یازده و چهل و چهار دقیقه و سی و سه ثانیه
        res = re.sub(fr'\b(?:{self.MINUTES_LIST})', lambda m: str(self.MINUTES[m.group()]), str(text))
        res = self.normalize_space(res)
        res = self.time_reformat(res) if self.time_reformat(res) is not None else res
        return res


extractor = ValueExtractor()

# d_sentence = "یک هزار و سیصد و هفت مهرماه سوم آبان ۱۲۵۰ معادل پنجاه قمری و هزار شمسی و سیمرغ نگاه بیست و یک و سوم آبان"
# q = extractor.compute_date_value(d_sentence)
# print("Compute Date value")
# print(q)

t_sentence = "۶۰ دهه "
q = extractor.compute_time_value(t_sentence)
print("Compute Time value")
print(q)
