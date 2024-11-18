from typing import List, Dict
import numpy as np

def calculate_divergences(corpora: List[Dict[str, int]], alpha: float) -> np.ndarray:
  """
  Optimized function for calculating pairwise divergences between multiple corpora
  based on token rank frequencies and a divergence sensitivity parameter (alpha).
  
  Args:
    corpora (List[Dict[str, int]]): List of dictionaries where each dictionary contains
      ngrams as keys and their frequencies as values.
    alpha (float): Sensitivity parameter that modifies the emphasis on frequency 
      differences between ngrams.

  Returns:
    np.ndarray: 3D numpy array of shape (num_ngrams, num_corpora, num_corpora) representing 
      the divergence matrix, with each element indicating the divergence between two corpora 
      for a given ngram.
  """
  normalization_value: float = calculate_normalization(corpora, alpha)
  full_normalization: float = (alpha + 1) / (alpha * normalization_value)

  # Aggregate all unique ngrams and create a mapping for indexing
  total_ngrams = list(set().union(*[corpus.keys() for corpus in corpora]))
  num_ngrams, num_corpora = len(total_ngrams), len(corpora)
  ngram_index = {ngram: idx for idx, ngram in enumerate(total_ngrams)}

  # Build rank matrix with shape (num_ngrams, num_corpora)
  rank_matrix = np.full((num_ngrams, num_corpora), fill_value=2 * (num_ngrams - len(set.intersection(*[set(c.keys()) for c in corpora]))))
  for j, corpus in enumerate(corpora):
    for ngram, rank in corpus.items():
      rank_matrix[ngram_index[ngram], j] = rank

  # Apply alpha power to rank matrix for divergence weighting
  rank_matrix_alpha = np.power(rank_matrix, alpha)

  # Use broadcasting to calculate pairwise differences for each ngram
  divergence_matrix = np.abs(rank_matrix_alpha[:, :, None] - rank_matrix_alpha[:, None, :])
  divergence_matrix = np.power(divergence_matrix, 1 / (1 + alpha))

  # Apply normalization
  divergence_matrix *= full_normalization

  return divergence_matrix, ngram_index

def calculate_normalization(corpora: List[Dict[str, int]], alpha: float) -> float:
  """
  Optimized function to compute normalization value based on token ranks across corpora 
  and a specified alpha.

  Args:
    corpora (List[Dict[str, int]]): List of dictionaries where each dictionary represents 
      a corpus, mapping tokens to their frequency ranks.
    alpha (float): Sensitivity parameter for weighting token frequency ranks.

  Returns:
    float: Normalization value for consistent divergence scaling across corpora and alpha values.
  """
  corpus_lengths = np.array([len(corpus) for corpus in corpora])
  avg_corpus_length = np.mean(corpus_lengths)

  normalization_value = 0.0
  for corpus in corpora:
    for rank in corpus.values():
      token_contrib = np.abs(
          1 / (rank ** alpha) - 
          1 / ((len(corpus) + avg_corpus_length) ** alpha)
      ) ** (1 / (1 + alpha))
      normalization_value += token_contrib

  return normalization_value
