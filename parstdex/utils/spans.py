import re


def merge_spans(spans, spans_key):
    result = []
    pos = {
        'start': 0,
        'end': 1
    }
    # sort by start
    zipped = list(zip(spans, spans_key))
    zipped_sorted = sorted(zipped, key= lambda x: (x[0][0], x[0][1] - x[0][0]))

    spans = [s for s, _ in zipped_sorted]
    spans_key = [k for _, k in zipped_sorted]

    spans.append((spans[-1][pos['end']], spans[-1][pos['end']]))
    spans_key.append(spans_key[-1])

    i = 0
    while i < len(spans) - 1:
        # end(i) < start(i+1)
        if spans[i][pos['end']] < spans[i + 1][pos['start']]:
            result.append(spans[i])
        # end(i)>=start(i+1)
        else:
            j = i
            max_end = spans[j][pos['end']]
            while max_end >= spans[j + 1][pos['start']]:
                j += 1
                if spans[j][pos['end']] > max_end:
                    max_end = spans[j][pos['end']]
                if j == len(spans) - 1:
                    break
            result.append((spans[i][pos['start']], max_end))
            i = j

        i += 1

    return result


def create_spans(normalized_sentence, patterns):
    # add pattern keys to dictionaries and define a list structure for each key
    output_raw = {}
    for key in patterns.regexes.keys():
        output_raw[key]: list = []

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

    spans = []
    spans_key = []
    for key in output_raw.keys():
        matches = output_raw[key]
        for match in matches:
            start = match.regs[0][0]
            end = match.regs[0][1]
            # match.group()
            spans.append((start, end))
            spans_key.append(key)

    return output_raw, spans, spans_key


def subtract_spans(normal_spans, adv_spans):
    """
    Subtract Spans example
    :param normal_spans: e.g. [(0, 15), (26, 35), (37, 42)]
    :param adv_spans: e.g. [(3, 10)]
    :return: e.g. [(0, 2), (11,15), (26, 35), (37, 42)]

    :param normal_spans: e.g. [(0, 15), (26, 35), (37, 42)]
    :param adv_spans: e.g. [(12, 18)]
    :return: e.g. [(0, 11), (26, 35), (37, 42)]

    :param normal_spans: e.g. [(0, 15), (18, 35), (37, 42)]
    :param adv_spans: e.g. [(12, 22)]
    :return: e.g. [(0, 11), (23, 35), (37, 42)]
    """
    pass


def find_spans(encoded_sent):
    spans = []
    i = 0
    while i <= len(encoded_sent):
        if encoded_sent[i] == 0:
            i += 1
            continue
        else:
            start = i
            j = start
            while j < len(encoded_sent) and encoded_sent[j] == 1:
                j += 1
            end = j - 1
            i = j + 1
            spans.append((start, end))
    return spans
