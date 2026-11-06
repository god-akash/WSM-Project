def search(query, index, tokenize_function, normalize_function, require_all=False):
    query_tokens = normalize_function(tokenize_function(query))

    # Unique words, order preserved
    words = list(dict.fromkeys(token["word"] for token in query_tokens))
    words = [w for w in words if w in index]

    if not words:
        return {}

    if require_all:
        # Only documents that contain every query word
        # (also fail if any query word is missing from the index)
        if len(words) != len(dict.fromkeys(t["word"] for t in query_tokens)):
            return {}
        doc_sets = [set(index[w]) for w in words]
        candidate_docs = set.intersection(*doc_sets)
    else:
        candidate_docs = set().union(*(index[w].keys() for w in words))

    results = {}
    for doc in candidate_docs:
        positions = []
        for w in words:
            positions.extend(index[w].get(doc, []))
        positions.sort(key=lambda p: p["start"])
        results[doc] = positions

    return results