import re


def merge_spans(spans, normalized_sentence):

    result = {
        "Date": [],
        "Time": []
    }

    encoded_date = encode_span(spans['Date'], spans['Adversarial'], normalized_sentence)
    encoded_time = encode_span(spans['Time'], spans['Adversarial'], normalized_sentence)

    result['Date'] = find_spans(encoded_date)
    result['Time'] = find_spans(encoded_time)

    return result


def create_spans(patterns, normalized_sentence):
    # add pattern keys to dictionaries and define a list structure for each key
    output_raw = {}
    spans = {}
    for key in patterns.regexes.keys():
        output_raw[key]: list = []
        spans[key]: list = []

    # apply regexes on normalized sentence and store extracted markers in output_raw
    for key in patterns.regexes.keys():
        for regex_value in patterns.regexes[key]:
            # apply regex
            out = re.findall(fr'\b(?:{regex_value})', normalized_sentence)
            # ignore empty markers
            if len(out) > 0:
                matches = list(re.finditer(fr'\b(?:{regex_value})', normalized_sentence))
                # store extracted markers in output_raw
                output_raw[key] = output_raw[key] + matches

    for key in output_raw.keys():
        matches = output_raw[key]
        for match in matches:
            start = match.regs[0][0]
            end = match.regs[0][1]
            # match.group()
            spans[key].append((start, end))

    return output_raw, spans


def encode_span(normal_spans, adv_spans, normalized_sentence):
    encoded_sent = [0] * len(normalized_sentence)

    for span in normal_spans:
        for i in range(span[0], span[1] + 1):
            encoded_sent[i] = 1

    for span in adv_spans:
        for i in range(span[0], span[1] + 1):
            encoded_sent[i] = 0

    return encoded_sent


def find_spans(encoded_sent):
    spans = []
    i = 0
    while i < len(encoded_sent):
        if encoded_sent[i] == 0:
            i += 1
            continue
        else:
            start = i
            while i < len(encoded_sent) and encoded_sent[i] == 1:
                i += 1
            end = i - 1
            i = i + 1
            spans.append((start, end))
    return spans
