import re

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
    if granularity == "all":
        return [i for i in synonyms if i.lower() != word.lower()]
    else:
        pass


def enhance_prompt(words: str) -> str:
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


import sqlite3
from typing import Dict, List


def find_words_in_fts(
    sentence: str, db_name: str, fts_table: str
) -> Dict[str, List[Dict]]:

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    words = sentence.split()
    word_results = {}

    for word in words:
        print(word)
        cursor.execute(
            f"""
        SELECT * FROM {fts_table} WHERE {fts_table} MATCH ?
        """,
            (word,),
        )
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        formatted_results = [dict(zip(column_names, result)) for result in results]

        ignore_list = [
            "and",
        ]
        if word in ignore_list:
            word_results[word] = [{}]

        elif formatted_results:
            # Without subsetting by organism formatted_results is too large
            # As PoC selecting only the first hit is good enough
            word_results[word] = formatted_results[0]
        else:
            word_results[word] = ""

    conn.close()
    return word_results


def knowledge_to_prompt(word_value_pairs):
    # Consumes output of find_words_in_fts
    ans = ""
    for k, v in word_value_pairs.items():
        ans += k + " "
        if isinstance(v, list) and len(v) == 1 and v[0] == {}:
            continue
        else:
            temp = "with synonyms "
            for kk, vv in v.items():
                temp += kk + " : " + str(vv) + ", "
            ans += temp
    return ans
