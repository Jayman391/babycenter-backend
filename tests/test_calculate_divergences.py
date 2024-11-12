import numpy as np
import pytest
from typing import List, Dict

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from babycenter_backend.allotax import calculate_divergences, calculate_normalization

# Assume calculate_divergences and calculate_normalization have been imported

def test_calculate_divergences_basic():
    """Test basic functionality and output shape for calculate_divergences."""
    corpora = [
        {"apple": 1, "banana": 2, "cherry": 3},
        {"apple": 2, "banana": 1, "cherry": 3},
        {"apple": 3, "banana": 2, "cherry": 1}
    ]
    alpha = 1
    divergence_matrix = calculate_divergences(corpora, alpha)

    # assert diagonals are zero
    assert np.all(np.diag(divergence_matrix[0]) == 0), "Divergence within a single corpus should be zero"
    # Basic assertions to ensure correct output type and shape
    assert isinstance(divergence_matrix, np.ndarray), "Output should be a numpy array"
    assert divergence_matrix.shape == (3, 3, 3), "Output shape should be (num_ngrams, num_corpora, num_corpora)"


def test_calculate_divergences_single_corpus():
    """Test calculate_divergences with a single corpus."""
    corpora = [{"apple": 1, "banana": 2}]
    alpha = 0.5
    divergence_matrix = calculate_divergences(corpora, alpha)

    assert divergence_matrix.shape == (2, 1, 1), "Output shape should be (num_ngrams, 1, 1) for single corpus"
    assert np.all(divergence_matrix == 0), "Divergence within a single corpus should be zero"

def test_calculate_divergences_non_overlapping_ngrams():
    """Test calculate_divergences with non-overlapping ngrams across corpora."""
    corpora = [
        {"apple": 1, "banana": 2},
        {"cherry": 1, "date": 2}
    ]
    alpha = 0.5
    divergence_matrix = calculate_divergences(corpora, alpha)

    assert divergence_matrix.shape == (4, 2, 2), "Output shape should account for all unique ngrams"
    assert np.all(divergence_matrix >= 0), "All divergences should be non-negative"


def test_calculate_normalization_basic():
    """Test basic normalization calculation."""
    corpora = [
        {"apple": 1, "banana": 2},
        {"apple": 2, "banana": 1}
    ]
    alpha = 1.0
    normalization_value = calculate_normalization(corpora, alpha)

    assert isinstance(normalization_value, float), "Normalization value should be a float"
    assert normalization_value > 0, "Normalization value should be positive"
