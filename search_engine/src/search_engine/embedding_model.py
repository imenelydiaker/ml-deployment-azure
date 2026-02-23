"""Sentence embedding model wrapper with caching and batch support."""

import logging

import numpy as np
from sentence_transformers import SentenceTransformer, util

from search_engine.config import settings

logger = logging.getLogger(__name__)


class EmbeddingModel:
    """Thin wrapper around SentenceTransformer with convenience methods."""

    def __init__(self, model_name: str | None = None):
        name = model_name or settings.model_name
        logger.info("Loading sentence-transformer model: %s", name)
        self.model = SentenceTransformer(name)
        self.model_name = name
        logger.info("Model loaded successfully")

    def encode(self, sentences: str | list[str]) -> np.ndarray:
        """Encode one or many sentences into embeddings.

        Returns:
            np.ndarray of shape (n, dim) – always 2-D even for a single sentence.
        """
        if isinstance(sentences, str):
            sentences = [sentences]
        embeddings = self.model.encode(sentences, convert_to_numpy=True, show_progress_bar=False)
        return np.atleast_2d(embeddings)

    def similarity(self, sentence1: str, sentence2: str) -> float:
        """Compute cosine similarity between two sentences."""
        emb1 = self.model.encode(sentence1, convert_to_numpy=True)
        emb2 = self.model.encode(sentence2, convert_to_numpy=True)
        score = util.cos_sim(emb1, emb2)
        return float(score.numpy()[0][0])
