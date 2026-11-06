from query_processor import search
from wildcard import wildcard_search


def boolean_search(query, index, tokenize_function, normalize_function):
    """
    Supports AND, OR (must be written in CAPITAL letters).
    Wildcards (* and ?) work inside any term.

    Examples:
        apple AND banana
        apple OR banana
        inform* AND retriev*
        apple AND banana OR cherry   ->  (apple AND banana) OR cherry

    AND is applied before OR.
    Words with no operator between them are treated as AND.
    """

    def run_term(term):
        if "*" in term or "?" in term:
            return wildcard_search(term, index, normalize_function)
        return search(term, index, tokenize_function, normalize_function)

    # Split the query into OR groups
    groups = [[]]
    for word in query.split():
        if word == "OR":
            groups.append([])
        elif word == "AND":
            continue
        else:
            groups[-1].append(word)

    final = {}

    for group in groups:
        if not group:
            continue

        group_results = None

        for term in group:
            found = run_term(term)

            if group_results is None:
                group_results = found
            else:
                # AND: keep only documents that contain both
                group_results = {
                    doc: group_results[doc] + found[doc]
                    for doc in group_results
                    if doc in found
                }

        # OR: add this group's documents to the final result
        for doc, positions in (group_results or {}).items():
            final.setdefault(doc, []).extend(positions)

    # Remove duplicate hits and sort by character position
    for doc in final:
        unique = {p["word_index"]: p for p in final[doc]}
        final[doc] = sorted(unique.values(), key=lambda p: p["start"])

    return final