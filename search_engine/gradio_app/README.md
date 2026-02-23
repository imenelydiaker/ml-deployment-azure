# Semantic Search Engine — Gradio UI

A Gradio web interface for the [Semantic Search Engine API](../README.md).

## Features

- **Similarity** — compare two sentences and see their cosine similarity score
- **Corpus management** — add sentences, check status, or clear the index
- **Semantic search** — search the corpus with natural language queries

## Setup

```bash
cd gradio_app

# Create virtualenv and install
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Usage

1. **Start the search engine API** (in another terminal):
   ```bash
   cd .. && uvicorn main:app --port 3000
   ```

2. **Start the Gradio app**:
   ```bash
   python app.py
   ```
   Opens at [http://localhost:7860](http://localhost:7860).

3. **Custom API URL**:
   ```bash
   SEARCH_API_URL=http://myhost:3000 python app.py
   ```

## Workflow

1. Open the **Corpus** tab → paste sentences (one per line) → click **Add to Corpus**
2. Switch to the **Search** tab → type a query → click **Search**
3. Use the **Similarity** tab for quick pairwise comparisons
