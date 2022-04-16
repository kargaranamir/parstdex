def tokenize_words(text):
    token_list = text.strip().split()
    token_list = [x.strip("\u200c") for x in token_list if len(x.strip("\u200c")) != 0]
    return token_list