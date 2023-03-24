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
