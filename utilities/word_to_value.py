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

    FA_NUMBERS = "۰|۱|۲|۳|۴|۵|۶|۷|۸|۹"
    EN_NUMBERS = "0|1|2|3|4|5|6|7|8|9"
    Symbols = ":|/|-"
    C_NUMBERS = FA_NUMBERS + "|" + EN_NUMBERS + "|" + Symbols

    JOINER = 'و'

    Units = "|".join(
        list(TEN_PLUS_TEXT.keys()) + list(HUNDREDS_TEXT.keys()) + list(MAGNITUDE.keys()) + list(
            TENS_TEXT.keys()) + list(
            ONES_TEXT.keys()) + list(TYPO_LIST.keys()))

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

    def compute_date_value(self, text):
        text = self.normalize_numbers(text)
        res = re.sub(fr'\b(?:{self.Units}|\s{self.JOINER}\s|\s|\d{1, 4})+\b', lambda m: str(self.convert_word_to_digits(m.group())), text)
        res = self.normalize_space(res)
        return res

    def compute_time_value(self, text):
        pass


extractor = ValueExtractor()

d_sentence = "یک هزار و سیصد و هفت مهرماه سوم آبان ۱۲۵۰ معادل پنجاه قمری و هزار شمسی و سیمرغ نگاه بیست و یک و سوم آبان"

q = extractor.compute_date_value(d_sentence)
print(q)

t_sentence = "ساعت بیست و یک و سی و چهار دقیقه و چهل و یک ثانیه می‌بینمت"
q = extractor.compute_time_value(d_sentence)
print(q)

TYPE_DATA = 0 # 0 for SHAMSI, 1 for GHAMARI, 2 for MILDAI

date_sentence = " 19 بهمن 1299"
MONTH_LIT = 'ماه'
YEAR_LIT = 'سال'


SHAMSI_LIST = '|'.join(list(extractor.SHAMSHI_MONTHS.keys()))
GHAMARI_LIST = '|'.join(list(extractor.GHAMARI_MONTHS.keys()))
MILADI_LIST = '|'.join(list(extractor.MILADI_MONTHS.keys()))

date_reg = fr'(\d+) ({SHAMSI_LIST})\s*[(?:{MONTH_LIT})]*\s*[(?:{YEAR_LIT})]* (\d+)'
print(date_reg)
date_result = re.search(date_reg, date_sentence).groups()
print(date_result)

HOUR_LIT = 'ساعت'
MIN_LIT = 'دقیقه'
SEC_LIT = 'ثانیه'
time_sentence = 'ساعت بیست و دو و سی و پنج دقیقه و چهل و یک ثانیه'
time_reg = fr'{HOUR_LIT}\s*(\d+)\s*[(?:{MIN_LIT})]\s*(\d)*\s*[(?:{SEC_LIT})]\s*(\d)*'
print(time_reg)
time_result = re.search(time_reg, time_sentence).groups()
print(time_result)






