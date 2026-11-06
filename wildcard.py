import re


def wildcard_to_regex(pattern):
    parts = []
    for ch in pattern:
        if ch == "*":
            parts.append(".*")
        elif ch == "?":
            parts.append(".")
        else:
            parts.append(re.escape(ch))
    return re.compile("".join(parts))


def wildcard_search(query, index, normalize_function):
    query = query.strip()

    # Lowercase the query using the same function used for indexing
    query = normalize_function(
        [{"word": query, "start": 0, "end": len(query)}]
    )[0]["word"]

    regex = wildcard_to_regex(query)

    results = {}
    for word, documents in index.items():
        if regex.fullmatch(word):
            for doc, positions in documents.items():
                results.setdefault(doc, []).extend(positions)

    for positions in results.values():
        positions.sort(key=lambda p: p["start"])

    return results