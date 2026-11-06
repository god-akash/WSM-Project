import re


def tokenize(text):
    """
    Tokenize the document while keeping the exact
    character position of every word.
    """

    tokens = []

    for match in re.finditer(r"\b\w+(?:['-]\w+)*\b", text):

        tokens.append({
            "word": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    return tokens