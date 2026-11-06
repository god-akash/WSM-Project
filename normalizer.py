def normalize(tokens):
    """
    Convert all tokens to lowercase while
    preserving their original positions.
    """

    normalized_tokens = []

    for token in tokens:

        normalized_tokens.append({
            "word": token["word"].lower(),
            "start": token["start"],
            "end": token["end"]
        })

    return normalized_tokens