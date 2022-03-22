import re
from typing import Dict


def merge_spans(spans: Dict, normalized_sentence: str):
    result, encoded = dict(), dict()

    encoded['Date'] = encode_span(spans['Date'],
                                  spans['Adversarial'],
                                  normalized_sentence)

    encoded['Time'] = encode_span(spans['Time'],
                                  spans['Adversarial'],
                                  normalized_sentence)

    encoded['Date'], encoded['Time'] = encode_rtl(encoded['Date'], encoded['Time'])

    encoded['Date'] = encode_space(encoded['Date'], spans['Space'])
    encoded['Time'] = encode_space(encoded['Time'], spans['Space'])

    result['Date+Time'] = find_spans(merge_encodes(encoded['Time'], encoded['Date']))
    result['Date'] = find_spans(encoded['Date'])
    result['Time'] = find_spans(encoded['Time'])

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
            out = re.findall(fr'\b(?:{regex_value})\b', normalized_sentence)
            # ignore empty markers
            if len(out) > 0:
                matches = list(re.finditer(fr'\b(?:{regex_value})\b', normalized_sentence))
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
        for i in range(span[0], span[1]):
            encoded_sent[i] = 1

    for span in adv_spans:
        for i in range(span[0], span[1]):
            encoded_sent[i] = 0
    return encoded_sent


def find_spans(encoded_sent):
    spans = []
    i: int = 0
    len_sent = len(encoded_sent)

    while i < len_sent:
        # ignore if it starts with 0 or -1
        if encoded_sent[i] == 0 or encoded_sent[i] == -1:
            i += 1
            continue
        else:
            # it means it starts with 1
            start = i
            end = i + 1
            # continue if you see 1 or -1
            while i < len_sent and (encoded_sent[i] == 1 or encoded_sent[i] == -1):
                # store the last time you see 1
                if encoded_sent[i] == 1:
                    end = i + 1
                i += 1

            spans.append((start, end))
    return spans


def encode_rtl(encoded_date, encoded_time):
    i = 0
    while i < len(encoded_date):

        if encoded_date[i] == 1 and encoded_time[i] == 1:

            if encoded_time[i - 1] == 1 and encoded_date[i - 1] == 0:
                while encoded_time[i] == 1:
                    encoded_date[i] = 0
                    if i < len(encoded_time) - 1:
                        i += 1
                    else:
                        break
            elif encoded_time[i - 1] == 0 and encoded_date[i - 1] == 1:
                while encoded_date[i] == 1:
                    encoded_time[i] = 0
                    if i < len(encoded_date) - 1:
                        i += 1
                    else:
                        break

            else:
                # start = i
                # while encoded_time[i] == 1 or encoded_date[i] == 1:
                #
                # TODO
                print("#TODO")
                print(f"Encoded Date:\n {encoded_date}")
                print(f"Encoded Date:\n {encoded_time}")
                i += 1
        else:
            i += 1
    return encoded_date, encoded_time


def encode_space(encoded_sent, space_spans):
    for span in space_spans:
        for i in range(span[0], span[1]):
            encoded_sent[i] = -1

    return encoded_sent


def sgn(num: int):
    if num >= 1:
        return 1
    elif num <= -1:
        return -1
    else:
        return 0


def merge_encodes(encoded_time, encoded_date):
    sum_encoded = [sgn(a+b) for a, b in zip(encoded_time, encoded_date)]
    return sum_encoded