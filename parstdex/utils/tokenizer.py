import re


# persian-english word tokenizer
def tokenize_words(text):
    text = re.sub(r"(\d+(?:\.\d+)?)", r" \1 ", text)
    token_list = re.findall(r"[\w\u200c']+|[!\"#$%&\'()*+,-./:؛؟،;<=>?@[\\\]^_`{|}~]", text)
    token_list = [x.strip("\u200c") for x in token_list if len(x.strip("\u200c")) != 0]
    return token_list
