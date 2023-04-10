import re
import sqlite3
from typing import Dict, List

synonyms = [
    "C3H7NO3",
    "L-serine",
    "serine",
    "CHEBI:17115",
    "(S)-2-Amino-3-hydroxypropanoic acid",
    "(S)-Serine",
]

synonyms = [i.lower() for i in synonyms]


def select_synonyms(word: str, synonyms: list[str], granularity: str = "all"):
    """Deprecated"""
    if granularity == "all":
        return [i for i in synonyms if i.lower() != word.lower()]
    else:
        pass


def enhance_prompt(words: str) -> str:
    """Deprecated"""
    pattern = r".*\baction::enhance\b.*"

    if not re.match(pattern, words):
        return words

    ans = []
    for word in words.split():
        if word == "action::enhance":
            continue
        elif word.lower() in synonyms:
            selected_synonyms = select_synonyms(word, synonyms)
            ans += [word, f"(synonyms are: {selected_synonyms})"]
        else:
            ans += [word]

    return " ".join(ans)


def enrich_metabolite_information(
    sentence: str,
    db_name: str = "collections.sqlite",
    fts_table: str = "pathbank_all_metabolites_fts",
):
    """
    Enriches a given sentence with metabolite information if it contains the 'action::enhance' pattern.
    """

    pattern = r".*\baction::enhance\b.*"

    if not re.match(pattern, sentence):
        return sentence
    sentence = sentence.replace("action::enhance", "")
    print(sentence)
    word_value_pairs = find_words_in_fts(sentence, db_name, fts_table)
    return knowledge_to_prompt(word_value_pairs)


def escape_fts5_special_chars(search_term: str) -> str:
    """
    Escapes FTS5 special characters in the given search term by surrounding each special character with double quotes.
    """
    fts5_special_chars = {
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        '"',
        "^",
        "-",
        "|",
        "@",
        "~",
        "&",
        "*",
        ":",
        ".",
    }

    # Check if any special characters are present in the search term
    if not any(char in search_term for char in fts5_special_chars):
        return search_term

    escaped_search_term = ""
    for char in search_term:
        if char in fts5_special_chars:
            escaped_search_term += f'"{char}"'
        else:
            escaped_search_term += char

    return escaped_search_term


def find_words_in_fts(
    sentence: str, db_name: str, fts_table: str
) -> Dict[str, List[Dict]]:
    # We have two challenges:
    # 1. Go through each word in sentence to find molecule and thus id and pythway info
    # TODO Add missing project
    # 2. Take a sentence and match all model organisms.
    # Take the respective main group e.g. bacteria for e.coli
    # use it to limit the search space in fts table
    # TODO Extract matched model org. Save it and reduce search space

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    words = sentence.split()
    word_results = {}

    for word in words:
        search_term = escape_fts5_special_chars(word)
        cursor.execute(
            f"""
        SELECT * FROM {fts_table} WHERE {fts_table} MATCH ?
        """,
            (search_term,),
        )
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        formatted_results = [dict(zip(column_names, result)) for result in results]

        ignore_list = [
            "and",
        ]
        if word in ignore_list or len(word) <= 4:
            word_results[word] = ""

        elif formatted_results:
            # Without subsetting by organism formatted_results is too large
            # As PoC selecting only the first hit is good enough
            word_results[word] = formatted_results[0]
        else:
            word_results[word] = ""

    conn.close()
    return word_results


def knowledge_to_prompt(word_value_pairs):
    # Consumes output of find_words_in_fts injects them into prompt
    ans = ""
    for k, v in word_value_pairs.items():
        ans += k + " "
        if isinstance(v, list) and len(v) == 1 and v[0] == {}:
            continue
        elif isinstance(v, dict):  # Check if v is a dictionary
            temp = ", also referred to as: "
            for kk, vv in v.items():
                temp += kk + " : " + str(vv) + ", "
            ans += temp
    return ans
