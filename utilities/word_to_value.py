import re
import utilities.const as const


class ValueExtractor:
    SHAMSHI_MONTHS = const.SHAMSHI_MONTHS
    GHAMARI_MONTHS = const.GHAMARI_MONTHS
    MILADI_MONTHS = const.MILADI_MONTHS

    ONES_TEXT = const.ONES_TEXT
    TENS_TEXT = const.TENS_TEXT
    TEN_PLUS_TEXT = const.TEN_PLUS_TEXT
    HUNDREDS_TEXT = const.HUNDREDS_TEXT
    MAGNITUDE = const.MAGNITUDE

    TYPO_LIST = const.TYPO_LIST

    FA_TO_EN = const.FA_TO_EN

    MINUTES = const.MINUTES
    HOUR_PART = const.HOUR_PART

    HOUR_PART_JOIN = "|".join(
        HOUR_PART.keys()
    )

    NEG_DURATION_JOIN = "|".join(
        ["به", "مانده به", "قبل", "قبل از", "پیش از"]
    )

    POS_DURATION_JOIN = "|".join(
        ["بعد", "پس از", "بعد از"]
    )

    DAY_PART_JOIN = '|'.join(
        ["شب", "شامگاه", "غروب", "بعد از ظهر", "بعدازظهر", "بعداز ظهر", "عصر", "صبح", "بامداد", "ظهر"]
    )
    PM_PART_LIST = ["شب", "شامگاه", "غروب", "بعد از ظهر", "بعدازظهر", "بعداز ظهر", "عصر"]

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
        PM = False
        for part_night in self.PM_PART_LIST:
            if part_night in text:
                PM = True

        # بیست دقیقه قبل از هفت
        try:
            reg = fr'(\d+)\s*(?:{self.MIN_LIT})\s*(?:{self.NEG_DURATION_JOIN})\s*(?:{self.HOUR_LIT})?\s*(\d+)\s*(?:{self.DAY_PART_JOIN})?'
            detected_time = re.search(reg, text).groups()
            hour = int(detected_time[1]) - 1
            minute = int(detected_time[0])
            if hour < 13 and PM:
                hour = hour + 12
            return f'{hour:02}:{(60 - minute):02}'
        except:
            pass

        # بیست دقیقه بعد از هفت
        try:
            reg = fr'(\d+)\s*(?:{self.MIN_LIT})\s*(?:{self.POS_DURATION_JOIN})\s*(?:{self.HOUR_LIT})?\s*(\d+)\s*(?:{self.DAY_PART_JOIN})?'
            detected_time = re.search(reg, text).groups()
            hour = int(detected_time[1])
            minute = int(detected_time[0])
            if hour < 13 and PM:
                hour = hour + 12
            return f'{hour:02}:{minute:02}'
        except:
            pass

        # یه ربع به شش
        try:
            reg = fr'({self.HOUR_PART_JOIN})\s*(?:{self.HOUR_LIT})?\s*(?:{self.NEG_DURATION_JOIN})\s*(?:{self.HOUR_LIT})?\s*(\d+)\s*(?:{self.DAY_PART_JOIN})?'
            detected_time = re.search(reg, text).groups()
            hour = int(detected_time[1]) - 1
            minute = self.HOUR_PART[detected_time[0]]
            if hour < 13 and PM:
                hour = hour + 12
            return f'{hour:02}:{(60 - minute):02}'
        except:
            pass

        # یه ربع بعد شش
        try:
            reg = fr'({self.HOUR_PART_JOIN})\s*(?:{self.HOUR_LIT})?\s*(?:{self.POS_DURATION_JOIN})\s*(?:{self.HOUR_LIT})?\s*(\d+)\s*(?:{self.DAY_PART_JOIN})?'
            detected_time = re.search(reg, text).groups()
            hour = int(detected_time[1])
            minute = self.HOUR_PART[detected_time[0]]
            if hour < 13 and PM:
                hour = hour + 12
            return f'{hour:02}:{minute:02}'
        except:
            pass


        try:
            # TODO: ساعت 9:54 ساعت ۰۹:۲۳
            reg = fr'(?:{self.HOUR_LIT})?\s*(\d+)(?:[{self.TIME_JOINER}])(\d*)\s*(?:[{self.TIME_JOINER}])?(\d*)?'

            detected_time = re.search(reg, text).groups()
            hour = int(detected_time[0])
            minute = int(detected_time[1])
            second = int(detected_time[2] if detected_time[2] != '' else "0")
            if hour < 13 and PM:
                hour = hour + 12
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
            if hour < 13 and PM:
                hour = hour + 12
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
            if hour < 13 and PM:
                hour = hour + 12
            return f'{hour:02}:{minute:02}:{second:02}'
        except:
            pass

        #  بیست و یک و چهل و دو دقیقه و سی و دو ثانیه صبح
        try:
            reg = fr'(\d+)\s*[{self.JOINER}]?\s*(\d*)\s*(?:{self.MIN_LIT})?\s*[{self.JOINER}]?\s*(\d*)\s*(?:{self.SEC_LIT})?\s+(?:{self.DAY_PART_JOIN})'
            detected_time = re.search(reg, text).groups()
            hour = int(detected_time[0])
            minute = int(detected_time[1] if detected_time[1] != '' else "0")
            second = int(detected_time[2] if detected_time[2] != '' else "0")
            if hour < 13 and PM == True:
                hour = hour + 12
            return f'{hour:02}:{minute:02}:{second:02}'
        except:
            pass

        # 23 دقیقه و 40 ثانیه شب
        try:
            reg = fr'(\d+)\s*(?:{self.MIN_LIT})\s*[{self.JOINER}]?\s*(\d*)\s*(?:{self.SEC_LIT})?\s+(?:{self.DAY_PART_JOIN})'
            detected_time = re.search(reg, text).groups()
            hour = 0
            minute = int(detected_time[0])
            second = int(detected_time[1])
            if hour < 13 and PM:
                hour = hour + 12
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
        res = re.sub(fr'\b(?:{self.MINUTES_LIST})\b', lambda m: str(self.MINUTES[m.group()]), str(text))
        res = self.normalize_space(res)
        res = self.time_reformat(res) if self.time_reformat(res) is not None else res
        return res


extractor = ValueExtractor()

# d_sentence = "یک هزار و سیصد و هفت مهرماه سوم آبان ۱۲۵۰ معادل پنجاه قمری و هزار شمسی و سیمرغ نگاه بیست و یک و سوم آبان"
# q = extractor.compute_date_value(d_sentence)
# print("Compute Date value")
# print(q)

# t_sentence = "بیست و چهار دقیقه پس از ساعت هفت"
# q = extractor.compute_time_value(t_sentence)
# print("Compute Time value")
# print(q)
