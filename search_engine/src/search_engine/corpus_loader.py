"""Load sentences from the AG News dataset for corpus population."""

import logging

from datasets import load_dataset

from search_engine.config import settings

logger = logging.getLogger(__name__)


def load_corpus() -> list[str]:
    """Load a subset of AG News headlines and return a flat list of sentences.

    AG News is a small news-topic dataset (~120k train / ~7.6k test) that downloads
    almost instantly.  Each record has a 'text' field with a short news snippet.

    Controlled by:
        CORPUS_NUM_SAMPLES  – how many samples to load (default 500)
    """
    num_samples = settings.corpus_num_samples

    logger.info("Loading AG News dataset (first %d samples) …", num_samples)

    ds = load_dataset(
        "ag_news",
        split=f"test[:{num_samples}]",
    )

    sentences: list[str] = [row["text"].strip() for row in ds if row["text"].strip()]

    logger.info("Loaded %d sentences from AG News", len(sentences))
    return sentences
