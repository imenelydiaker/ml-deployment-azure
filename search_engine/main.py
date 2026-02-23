"""Semantic Search Engine API.

The corpus is auto-populated from the AG News dataset at startup.

Endpoints:
    GET  /           → welcome message
    GET  /health     → health check
    POST /similarity → cosine similarity between two sentences
    GET  /corpus         → corpus info
    GET  /corpus/browse  → paginated corpus sentences
    DELETE /corpus       → clear the corpus
    POST /search         → semantic search over the indexed corpus
"""

import sys
import logging

from fastapi import FastAPI, HTTPException

from search_engine.config import settings
from search_engine.corpus_loader import load_corpus
from search_engine.embedding_model import EmbeddingModel
from search_engine.index import SearchIndex
from search_engine.schemas import (
    CorpusBrowse,
    CorpusStatus,
    HealthResponse,
    SearchHit,
    SearchQuery,
    SearchResponse,
    SentencePair,
    SimilarityResult,
)

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    stream=sys.stdout,
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ── Startup ───────────────────────────────────────────────────────────────────

logger.info("Initializing embedding model (%s) …", settings.model_name)
embedding_model = EmbeddingModel()

logger.info("Creating search index …")
search_index = SearchIndex(model=embedding_model)

# ── Pre-populate corpus from AG News ──────────────────────────────────────────

logger.info("Loading corpus …")
_corpus_sentences = load_corpus()
logger.info("Indexing %d sentences into search index …", len(_corpus_sentences))
batch_size = settings.corpus_index_batch_size
for i in range(0, len(_corpus_sentences), batch_size):
    batch = _corpus_sentences[i : i + batch_size]
    search_index.index(batch)
    logger.info("  indexed %d / %d", min(i + batch_size, len(_corpus_sentences)), len(_corpus_sentences))
del _corpus_sentences
logger.info("Corpus ready — %d sentences indexed", search_index.size)

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="Compute semantic similarity and search over a sentence corpus.",
)
logger.info("API ready")


# ── Routes ────────────────────────────────────────────────────────────────────


@app.get("/")
def home():
    return {"message": f"Welcome to the {settings.app_title} API!"}


@app.get("/health", response_model=HealthResponse)
def health():
    """Liveness / readiness probe."""
    return HealthResponse(
        status="ok",
        model_loaded=True,
        corpus_size=search_index.size,
        model_name=embedding_model.model_name,
    )


@app.post("/similarity", response_model=SimilarityResult)
def similarity(pair: SentencePair):
    """Compute cosine similarity between two sentences."""
    score = embedding_model.similarity(pair.sentence1, pair.sentence2)
    logger.info("Similarity %.4f  |  '%s' ↔ '%s'", score, pair.sentence1[:60], pair.sentence2[:60])
    return SimilarityResult(sentence1=pair.sentence1, sentence2=pair.sentence2, score=round(score, 6))


# ── Corpus info ───────────────────────────────────────────────────────────────


@app.get("/corpus", response_model=CorpusStatus)
def corpus_info():
    """Return current corpus size and model info."""
    return CorpusStatus(size=search_index.size, model_name=embedding_model.model_name)


@app.get("/corpus/browse", response_model=CorpusBrowse)
def browse_corpus(offset: int = 0, limit: int = 20):
    """Return a paginated slice of corpus sentences."""
    limit = min(limit, 100)  # cap page size
    sentences = search_index.browse(offset=offset, limit=limit)
    return CorpusBrowse(
        total=search_index.size,
        offset=offset,
        limit=limit,
        sentences=sentences,
    )


@app.delete("/corpus", response_model=CorpusStatus)
def clear_corpus():
    """Remove all indexed sentences."""
    search_index.clear()
    return CorpusStatus(size=search_index.size, model_name=embedding_model.model_name)


# ── Search ────────────────────────────────────────────────────────────────────


@app.post("/search", response_model=SearchResponse)
def search(body: SearchQuery):
    """Search the indexed corpus for sentences most similar to the query."""
    try:
        hits = search_index.search(query=body.query, top_k=body.top_k)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return SearchResponse(
        query=body.query,
        total_corpus_size=search_index.size,
        results=[SearchHit(**h) for h in hits],
    )