from typing import Dict
import numpy as np

from parstdex.utils import regex_tool


def merge_spans(spans: Dict, normalized_sentence: str):
    result, encoded = dict(), dict()

    encoded['date'] = encode_span(spans['date'],
                                  spans['adversarial'],
                                  normalized_sentence)

    encoded['time'] = encode_span(spans['time'],
                                  spans['adversarial'],
                                  normalized_sentence)

    encoded['date'], encoded['time'] = encode_rtl_prv(encoded['date'], encoded['time'])
    encoded['date'], encoded['time'] = encode_rtl_nxt(encoded['date'], encoded['time'])

    encoded['date'] = encode_space(encoded['date'], spans['space'])
    encoded['time'] = encode_space(encoded['time'], spans['space'])

    result['datetime'] = find_spans(merge_encodings(encoded['time'], encoded['date']))
    result['date'] = find_spans(encoded['date'])
    result['time'] = find_spans(encoded['time'])

    return result


def create_spans(regexes, normalized_sentence):
    # add pattern keys to dictionaries and define a list structure for each key
    output_raw = {}
    spans = {}
    for key in regexes.keys():
        output_raw[key]: list = []
        spans[key]: list = []

    # apply regexes on normalized sentence and store extracted markers in output_raw
    for key in regexes.keys():
        for compiled_regex_val in regexes[key]:
            # apply regex
            matches = regex_tool.finditer(compiled_regex_val, normalized_sentence)
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

            spans.append([start, end])
    return spans


def encode_rtl_prv(encoded_date, encoded_time):
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
            # check which pattern has started sooner by margin of 3 spaces
            j = i - 1
            # no negative index for encoded strings
            if j < 0:
                i = i + 1
                continue
            while (encoded_time[j] == 0 and encoded_date[j] == 0) and j >= i - 3:
                if j == 0:
                    break
                j = j - 1
            if encoded_time[j] == 1 and encoded_date[j] == 0:
                # and remove 1 encoding from the latter detected pattern
                while encoded_time[i] == 1:
                    encoded_date[i] = 0
                    if i < len(encoded_time) - 1:
                        i += 1
                    else:
                        break
            elif encoded_time[j] == 0 and encoded_date[j] == 1:
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


def encode_rtl_nxt(encoded_date, encoded_time):
    """
    remove bad categorized encoded span
    :param encoded_date:
    :param encoded_time:
    :return:
    """
    i = 0
    while i < len(encoded_date):
        # if both time and date patterns exist
        if encoded_date[i] == 1 and encoded_time[i] == 1:
            start = i
            while encoded_date[i] == 1 and encoded_time[i] == 1:
                # check not to overflow from sentence len
                i += 1
                if i == len(encoded_date):
                    break
            end = i
            if end == len(encoded_date):
                encoded_time[start:end] = 0
            else:
                if encoded_time[end] != 1:
                    encoded_time[start:end] = 0
                else:
                    encoded_date[start:end] = 0
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
    merged_encoding = [sgn(a + b) for a, b in zip(encoded_time, encoded_date)]
    return merged_encoding


# a function to find the spans within an indices range
def filter_span_in_range(start_index, end_index, span_list):
    res = list(filter(lambda x: start_index <= x[0] and x[1] <= end_index, span_list))
    return sorted(res, key=lambda x: x[0])
