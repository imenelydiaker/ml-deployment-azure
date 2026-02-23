"""HTTP client for the Semantic Search Engine API."""

import httpx


class SearchEngineClient:
    """Typed wrapper around the search engine REST API."""

    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url.rstrip("/")

    # ── helpers ───────────────────────────────────────────────────────────

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    # ── endpoints ─────────────────────────────────────────────────────────

    def health(self) -> dict:
        """GET /health"""
        r = httpx.get(self._url("/health"), timeout=10)
        r.raise_for_status()
        return r.json()

    def similarity(self, sentence1: str, sentence2: str) -> dict:
        """POST /similarity"""
        r = httpx.post(
            self._url("/similarity"),
            json={"sentence1": sentence1, "sentence2": sentence2},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    def get_corpus(self) -> dict:
        """GET /corpus"""
        r = httpx.get(self._url("/corpus"), timeout=10)
        r.raise_for_status()
        return r.json()

    def clear_corpus(self) -> dict:
        """DELETE /corpus"""
        r = httpx.delete(self._url("/corpus"), timeout=10)
        r.raise_for_status()
        return r.json()

    def browse_corpus(self, offset: int = 0, limit: int = 20) -> dict:
        """GET /corpus/browse"""
        r = httpx.get(
            self._url("/corpus/browse"),
            params={"offset": offset, "limit": limit},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    def search(self, query: str, top_k: int = 5) -> dict:
        """POST /search"""
        r = httpx.post(
            self._url("/search"),
            json={"query": query, "top_k": top_k},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()
