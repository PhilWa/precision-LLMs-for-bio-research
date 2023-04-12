import pytest
from sentence_transformers import SentenceTransformer
from utils import calc_embeddings
import numpy as np


def test_calc_embeddings_default_model():
    """
    Test calc_embeddings using the default BERT model.
    """
    ans = "serine is important for cancer metabolism"
    embeddings = calc_embeddings(ans)

    model = SentenceTransformer("all-mpnet-base-v2")
    expected_embeddings = model.encode(ans)

    assert np.allclose(embeddings, expected_embeddings)


def test_calc_embeddings_sci_bert_model():
    """
    Test calc_embeddings using the Sci-BERT model.
    """
    ans = "serine is important for cancer metabolism"
    embeddings = calc_embeddings(ans, model_name="sci-bert")

    model = SentenceTransformer("allenai/scibert_scivocab_uncased")
    expected_embeddings = model.encode(ans)

    assert np.allclose(embeddings, expected_embeddings)


def test_calc_embeddings_invalid_model():
    """
    Test calc_embeddings with an invalid model name, expecting a ZeroDivisionError.
    """
    ans = "serine is important for cancer metabolism"
    with pytest.raises(ZeroDivisionError):
        calc_embeddings(ans, model_name="invalid_model")


def test_sentence_similarity_sci_bert():
    """
    Test sentence similarity using Sci-BERT by comparing the cosine similarity of their embeddings.
    """
    sentence1 = "The protein synthesis process is crucial for cellular function."
    sentence2 = "Protein production is vital for the functioning of cells."
    sentence3 = "The solar system consists of planets orbiting the Sun."

    # Calculate embeddings using Sci-BERT
    embeddings1 = calc_embeddings(sentence1, model_name="sci-bert")
    embeddings2 = calc_embeddings(sentence2, model_name="sci-bert")
    embeddings3 = calc_embeddings(sentence3, model_name="sci-bert")

    # Calculate cosine similarity
    similarity12 = np.dot(embeddings1, embeddings2) / (
        np.linalg.norm(embeddings1) * np.linalg.norm(embeddings2)
    )
    similarity13 = np.dot(embeddings1, embeddings3) / (
        np.linalg.norm(embeddings1) * np.linalg.norm(embeddings3)
    )

    # Check if the similarity between sentence1 and sentence2 is greater than the similarity between sentence1 and sentence3
    assert similarity12 > similarity13


if __name__ == "__main__":
    pytest.main([__file__])
