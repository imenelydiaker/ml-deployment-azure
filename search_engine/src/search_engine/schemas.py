"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field


# ── Requests ──────────────────────────────────────────────────────────────────


class SentencePair(BaseModel):
    """Two sentences to compare for similarity."""

    sentence1: str = Field(..., min_length=1, examples=["The cat sat on the mat."])
    sentence2: str = Field(..., min_length=1, examples=["A kitten rested on the rug."])


class SearchQuery(BaseModel):
    """A query to search against the indexed corpus."""

    query: str = Field(..., min_length=1, examples=["How does AI work?"])
    top_k: int = Field(default=5, ge=1, le=100, description="Number of results to return")


# ── Responses ─────────────────────────────────────────────────────────────────


class SimilarityResult(BaseModel):
    """Pairwise similarity score."""

    sentence1: str
    sentence2: str
    score: float = Field(..., ge=-1.0, le=1.0)


class SearchHit(BaseModel):
    """A single search result."""

    rank: int
    sentence: str
    score: float


class SearchResponse(BaseModel):
    """Search results for a query."""

    query: str
    total_corpus_size: int
    results: list[SearchHit]


class CorpusStatus(BaseModel):
    """Current state of the indexed corpus."""

    size: int
    model_name: str


class CorpusBrowse(BaseModel):
    """Paginated view of corpus sentences."""

    total: int
    offset: int
    limit: int
    sentences: list[str]


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    model_loaded: bool
    corpus_size: int
    model_name: str
