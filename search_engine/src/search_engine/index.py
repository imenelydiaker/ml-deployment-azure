"""In-memory vector index for semantic search over a sentence corpus."""

import logging

import numpy as np
from sentence_transformers import util

from search_engine.config import settings
from search_engine.embedding_model import EmbeddingModel

logger = logging.getLogger(__name__)


class SearchIndex:
    """Stores sentence embeddings and supports top-k semantic search."""

    def __init__(self, model: EmbeddingModel):
        self._model = model
        self._sentences: list[str] = []
        self._embeddings: np.ndarray | None = None  # shape (n, dim)

    @property
    def size(self) -> int:
        return len(self._sentences)

    def index(self, sentences: list[str]) -> int:
        """Add sentences to the corpus and compute their embeddings.

        Returns:
            The new total corpus size.

        Raises:
            ValueError: If adding these sentences would exceed *max_corpus_size*.
        """
        if self.size + len(sentences) > settings.max_corpus_size:
            raise ValueError(
                f"Corpus would exceed max size ({settings.max_corpus_size}). "
                f"Current: {self.size}, adding: {len(sentences)}. "
                "Clear the corpus first or increase MAX_CORPUS_SIZE."
            )

        new_embeddings = self._model.encode(sentences)
        self._sentences.extend(sentences)

        if self._embeddings is None:
            self._embeddings = new_embeddings
        else:
            self._embeddings = np.vstack([self._embeddings, new_embeddings])

        logger.info("Indexed %d sentences (total: %d)", len(sentences), self.size)
        return self.size

    def browse(self, offset: int = 0, limit: int = 20) -> list[str]:
        """Return a page of sentences from the corpus.

        Args:
            offset: Starting index (0-based).
            limit:  Maximum number of sentences to return.

        Returns:
            A list of sentence strings.
        """
        return self._sentences[offset : offset + limit]

    def clear(self) -> None:
        """Remove all sentences and embeddings from the index."""
        self._sentences.clear()
        self._embeddings = None
        logger.info("Corpus cleared")

    def search(self, query: str, top_k: int | None = None) -> list[dict]:
        """Return the *top_k* most similar sentences to *query*.

        Returns:
            A list of dicts with keys: rank, sentence, score.

        Raises:
            RuntimeError: If the corpus is empty.
        """
        if self.size == 0:
            raise RuntimeError("Corpus is empty. Index some sentences first via POST /corpus.")

        k = min(top_k or settings.default_top_k, self.size)
        query_embedding = self._model.encode(query)  # (1, dim)

        # Compute cosine similarities against the whole corpus
        scores = util.cos_sim(query_embedding, self._embeddings)[0]  # (n,)
        scores_np = scores.numpy()

        # Get top-k indices (descending)
        top_indices = np.argsort(scores_np)[::-1][:k]

        results = []
        for rank, idx in enumerate(top_indices, start=1):
            results.append(
                {
                    "rank": rank,
                    "sentence": self._sentences[idx],
                    "score": round(float(scores_np[idx]), 6),
                }
            )

        return results
