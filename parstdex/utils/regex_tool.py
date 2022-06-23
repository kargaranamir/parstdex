def finditer(compiled_regex, string):
    """Return an iterator over all non-overlapping matches in the
    string.  For each match, the iterator returns a Match object.

    Empty matches are included in the result."""
    return list(compiled_regex.finditer(string))
