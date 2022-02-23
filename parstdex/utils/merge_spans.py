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
