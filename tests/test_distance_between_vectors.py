import numpy as np
import pytest
from utils import distance_between_vector_and_vectors


def test_distance_between_vector_and_vectors_basic_case():
    """
    Test the cosine similarities between vector1 and vectors_array for basic 2D vectors,
    including orthogonal and parallel vectors.
    """
    vector1 = np.array([1, 0])
    vectors_array = np.array([[0, 1], [1, 0], [-1, 0], [0, -1]])

    similarities = distance_between_vector_and_vectors(vector1, vectors_array)

    assert np.allclose(similarities, np.array([0, 1, -1, 0]))


def test_distance_between_vector_and_vectors_identical_vectors():
    """
    Test the cosine similarities between vector1 and vectors_array for identical and scaled vectors.
    """
    vector1 = np.array([2, 3])
    vectors_array = np.array([[2, 3], [4, 6]])

    similarities = distance_between_vector_and_vectors(vector1, vectors_array)

    assert np.allclose(similarities, np.array([1, 1]))
