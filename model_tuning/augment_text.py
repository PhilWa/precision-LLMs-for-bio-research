import random
import nltk
from nltk.corpus import wordnet
from transformers import MarianMTModel, MarianTokenizer
from typing import Tuple


def augment_text(text: str, augmentations: int = 2) -> str:
    """
    Augments the input text by applying a randomly selected augmentation method.

    Args:
        text: The input text to be augmented.
        augmentations: The number of augmentations to be applied.

    Returns:
        The augmented text.
    """
    augmented_text = text
    for _ in range(augmentations):
        augmentation_methods = [
            synonym_replacement,
            random_deletion,
            random_swap,
            back_translate,
        ]
        selected_method = random.choice(augmentation_methods)
        if selected_method == back_translate:
            augmented_text = back_translate(
                augmented_text,
                tokenizer_en_fr,
                model_en_fr,
                tokenizer_fr_en,
                model_fr_en,
            )
        else:
            augmented_text = selected_method(augmented_text)
    return augmented_text


# Only needed the first time
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")

# English to French
src_lang_1 = "en"
tgt_lang_1 = "fr"
model_name_1 = f"Helsinki-NLP/opus-mt-{src_lang_1}-{tgt_lang_1}"

tokenizer_en_fr = MarianTokenizer.from_pretrained(model_name_1)
model_en_fr = MarianMTModel.from_pretrained(model_name_1)

# French to English
src_lang_2 = "fr"
tgt_lang_2 = "en"
model_name_2 = f"Helsinki-NLP/opus-mt-{src_lang_2}-{tgt_lang_2}"

tokenizer_fr_en = MarianTokenizer.from_pretrained(model_name_2)
model_fr_en = MarianMTModel.from_pretrained(model_name_2)


def back_translate(
    text: str, tokenizer_src_tgt, model_src_tgt, tokenizer_tgt_src, model_tgt_src
) -> str:
    """
    Back-translates the input text to improve the text's diversity.

    Args:
        text: The input text to be back-translated.
        tokenizer_src_tgt: Tokenizer for source to target language.
        model_src_tgt: Model for source to target language.
        tokenizer_tgt_src: Tokenizer for target to source language.
        model_tgt_src: Model for target to source language.

    Returns:
        The back-translated text.
    """
    encoded_text = tokenizer_src_tgt.encode(text, return_tensors="pt")
    translated_text = model_src_tgt.generate(encoded_text)
    tgt_text = tokenizer_src_tgt.decode(translated_text[0], skip_special_tokens=True)

    encoded_tgt_text = tokenizer_tgt_src.encode(tgt_text, return_tensors="pt")
    back_translated_text = model_tgt_src.generate(encoded_tgt_text)
    back_translated_src_text = tokenizer_tgt_src.decode(
        back_translated_text[0], skip_special_tokens=True
    )

    return back_translated_src_text


def translate(text: str, tokenizer, model) -> str:
    """
    Translates the input text to the target language.

    Args:
        text: The input text to be translated.
        tokenizer: Tokenizer for the translation model.
        model: Translation model.

    Returns:
        The translated text.
    """
    input_tokens = tokenizer.encode(text, return_tensors="pt")
    translated_tokens = model.generate(input_tokens)
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translated_text


# Synonym replacement
def synonym_replacement(sentence: str, num_replacements: int = 1) -> str:
    """
    Replaces a random word in the sentence with one of its synonyms.

    Args:
        sentence: The input sentence to be modified.

    Returns:
        The sentence with words replaced by synonyms.
    """
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)

    for _ in range(num_replacements):
        word_idx = random.choice(range(len(words)))
        word = words[word_idx]
        synsets = wordnet.synsets(word)

        if synsets:
            synonym = random.choice(synsets).lemmas()[0].name()
            words[word_idx] = synonym

    return " ".join(words)


# Random deletion
def random_deletion(sentence: str, p: float = 0.1) -> str:
    """
    Deletes words from the sentence randomly based on a given probability.
    Args:
        sentence: The input sentence to be modified.
        p: The probability of a word being deleted from the sentence.

    Returns:
        The sentence with words randomly deleted.
    """
    words = nltk.word_tokenize(sentence)
    remaining_words = [word for word in words if random.uniform(0, 1) > p]
    return " ".join(remaining_words)


# Random swap
def random_swap(sentence: str, num_swaps: int = 1) -> str:
    """
    Swaps two words in the sentence randomly.
    Args:
        sentence: The input sentence to be modified.
        num_swaps: The number of pairs of words to be swapped in the sentence.

    Returns:
        The sentence with words randomly swapped.
    """
    words = nltk.word_tokenize(sentence)

    for _ in range(num_swaps):
        idx1, idx2 = random.sample(range(len(words)), 2)
        words[idx1], words[idx2] = words[idx2], words[idx1]

    return " ".join(words)
