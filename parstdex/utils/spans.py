import re
from typing import Dict


def merge_spans(spans: Dict, normalized_sentence: str):
    result, encoded = dict(), dict()

    encoded['DateTime'] = encode_span(spans['DateTime'], spans['Adversarial'], normalized_sentence)
    encoded['Date'] = encode_span(spans['Date'], spans['Adversarial'] + spans['DateTime'], normalized_sentence)
    encoded['Time'] = encode_span(spans['Time'], spans['Adversarial'] + spans['DateTime'], normalized_sentence)
    encoded['Date'], encoded['Time'] = encode_rtl(encoded['Date'], encoded['Time'])

    result['Date'] = find_spans(encoded['Date'])
    result['Time'] = find_spans(encoded['Time'])
    result['DateTime'] = find_spans(encoded['DateTime'])

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
    encoded_sent = [0] * (len(normalized_sentence) + 1)

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
            elif encoded_date[i - 1] == 1 and encoded_time[i - 1] == 0:
                while encoded_date[i] == 1:
                    encoded_time[i] = 0
                    if i < len(encoded_date) - 1:
                        i += 1
                    else:
                        break

            else:
                # TODO
                print("#TODO")
                i += 1
        else:
            i += 1
    return encoded_date, encoded_time
