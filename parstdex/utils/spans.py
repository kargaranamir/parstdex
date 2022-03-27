import re
from typing import Dict
import numpy as np

from parstdex.utils import const


def merge_spans(spans: Dict, normalized_sentence: str):
    result, encoded = dict(), dict()

    encoded['date'] = encode_span(spans['date'],
                                  spans['adversarial'],
                                  normalized_sentence)

    encoded['time'] = encode_span(spans['time'],
                                  spans['adversarial'],
                                  normalized_sentence)

    encoded['date'], encoded['time'] = encode_rtl(encoded['date'], encoded['time'])

    encoded['date'] = encode_space(encoded['date'], spans['Space'])
    encoded['time'] = encode_space(encoded['time'], spans['Space'])

    result['datetime'] = find_spans(merge_encodings(encoded['time'], encoded['date']))
    result['date'] = find_spans(encoded['date'])
    result['time'] = find_spans(encoded['time'])

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
            matches = list(
                re.finditer(
                    fr'\b(?:{regex_value})(?:\b|(?!{const.FA_SYM}|\d+))',
                    normalized_sentence)
            )
            # ignore empty markers
            if len(matches) > 0:
                # store extracted markers in output_raw
                for match in matches:
                    start = match.regs[0][0]
                    end = match.regs[0][1]
                    spans[key].append((start, end))
                    output_raw[key].append(match)

    return output_raw, spans


def encode_span(normal_spans, adv_spans, normalized_sentence):
    encoded_sent = np.zeros(len(normalized_sentence))

    for span in normal_spans:
        encoded_sent[span[0]: span[1]] = 1

    for span in adv_spans:
        encoded_sent[span[0]: span[1]] = 0

    return encoded_sent


def find_spans(encoded_sent):
    """
    Find spans in a given encoding
    :param encoded_sent: list
    :return: list[tuple]
    """
    spans = []
    i: int = 0
    len_sent = len(encoded_sent)

    while i < len_sent:
        # ignore if it starts with 0(nothing matched) or -1(space)
        if encoded_sent[i] <= 0:
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
    """
    right to left prioritize mat
    :param encoded_date:
    :param encoded_time:
    :return:
    """
    i = 0
    while i < len(encoded_date):
        # if both time and date patterns exist
        if encoded_date[i] == 1 and encoded_time[i] == 1:
            # check which pattern has started sooner
            if encoded_time[i - 1] == 1 and encoded_date[i - 1] == 0:
                # and remove 1 encoding from the latter detected pattern
                while encoded_time[i] == 1:
                    encoded_date[i] = 0
                    if i < len(encoded_time) - 1:
                        i += 1
                    else:
                        break
            elif encoded_time[i - 1] == 0 and encoded_date[i - 1] == 1:
                # and remove 1 encoding from the latter detected pattern
                while encoded_date[i] == 1:
                    encoded_time[i] = 0
                    if i < len(encoded_date) - 1:
                        i += 1
                    else:
                        break
            # else if both are 0
            else:
                # debug may be required in future versions
                i += 1
        else:
            i += 1
    return encoded_date, encoded_time


def encode_space(encoded_sent, space_spans):
    """
    Encoded spaces to -1 in sentence encoding
    :param encoded_sent: list
    :param space_spans: list[tuple]
    :return: list
    """
    for span in space_spans:
        encoded_sent[span[0]: span[1]] = -1

    return encoded_sent


def sgn(num: int):
    if num >= 1:
        return 1
    elif num <= -1:
        return -1
    else:
        return 0


def merge_encodings(encoded_time, encoded_date):
    merged_encoding = [sgn(a+b) for a, b in zip(encoded_time, encoded_date)]
    return merged_encoding