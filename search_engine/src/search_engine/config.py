"""Application configuration loaded from environment variables with sensible defaults."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support.

    All settings can be overridden via environment variables, e.g.:
        MODEL_NAME=paraphrase-MiniLM-L6-v2  uvicorn main:app
    """

    model_name: str = "all-MiniLM-L6-v2"
    max_corpus_size: int = 10_000
    default_top_k: int = 5
    log_level: str = "INFO"
    app_title: str = "Semantic Search Engine"
    app_version: str = "0.1.0"

    # Corpus dataset settings
    corpus_num_samples: int = 500
    corpus_index_batch_size: int = 256

    model_config = {"env_prefix": "", "case_sensitive": False}


settings = Settings()
