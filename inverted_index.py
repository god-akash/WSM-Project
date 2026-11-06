def build_index(documents, tokenize_function, normalize_function):
    """
    Build an inverted index.

    Structure:

    {
        "information": {
            "doc1.txt": [
                {
                    "word_index": 0,
                    "start": 0,
                    "end": 11
                }
            ]
        }
    }
    """

    index = {}

    for document_name, text in documents.items():

        # Tokenize document
        tokens = tokenize_function(text)

        # Normalize tokens
        normalized_tokens = normalize_function(tokens)

        # Store each word with its position
        for word_index, token in enumerate(normalized_tokens):

            word = token["word"]

            if word not in index:
                index[word] = {}

            if document_name not in index[word]:
                index[word][document_name] = []

            index[word][document_name].append({
                "word_index": word_index,
                "start": token["start"],
                "end": token["end"]
            })

    return index