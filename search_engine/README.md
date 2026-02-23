# Semantic Search Engine

A FastAPI-based semantic search engine powered by [sentence-transformers](https://www.sbert.net/).  
Index a corpus of sentences and search for the most semantically similar ones using cosine similarity.

## Features

- **Pairwise similarity** — compute cosine similarity between any two sentences
- **Corpus indexing** — add sentences to an in-memory vector index
- **Semantic search** — find the top-k most similar sentences to a query
- **Configurable** — change model, corpus size, and more via environment variables

## Quick start

```bash
# Create a virtual environment and install
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Run the API
uvicorn main:app --reload --port 3000
```

## API endpoints

| Method   | Path          | Description                              |
|----------|---------------|------------------------------------------|
| `GET`    | `/`           | Welcome message                          |
| `GET`    | `/health`     | Health / readiness check                 |
| `POST`   | `/similarity` | Cosine similarity between two sentences  |
| `POST`   | `/corpus`     | Index sentences into the corpus          |
| `GET`    | `/corpus`     | Get corpus status                        |
| `DELETE` | `/corpus`     | Clear all indexed sentences              |
| `POST`   | `/search`     | Search the corpus for similar sentences  |

## Example usage

```bash
# Pairwise similarity
curl -X POST http://localhost:3000/similarity \
  -H "Content-Type: application/json" \
  -d '{"sentence1": "The cat sat on the mat", "sentence2": "A kitten rested on the rug"}'

# Index sentences
curl -X POST http://localhost:3000/corpus \
  -H "Content-Type: application/json" \
  -d '{"sentences": ["Machine learning is great", "Deep learning powers modern AI", "Python is popular"]}'

# Search
curl -X POST http://localhost:3000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence", "top_k": 3}'
```

## Configuration (environment variables)

| Variable           | Default              | Description                       |
|--------------------|----------------------|-----------------------------------|
| `MODEL_NAME`       | `all-MiniLM-L6-v2`  | Sentence-transformer model name   |
| `MAX_CORPUS_SIZE`  | `10000`              | Maximum sentences in the corpus   |
| `DEFAULT_TOP_K`    | `5`                  | Default number of search results  |
| `LOG_LEVEL`        | `INFO`               | Python logging level              |

## Docker

```bash
docker build -t search-engine .
docker run -p 3000:3000 search-engine
```