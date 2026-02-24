# ML Deployment on Azure

A collection of machine learning and AI projects designed to be deployed on **Microsoft Azure**. The repository demonstrates end-to-end workflows — from training models in Azure ML to serving inference via containerised APIs and interactive web UIs — using Azure AI services.

## Projects

| Project | Description | Key Technologies |
|---------|-------------|------------------|
| [**search_engine/**](search_engine/) | Semantic search API powered by sentence-transformers | FastAPI, sentence-transformers, Docker |
| [**search_engine/gradio_app/**](search_engine/gradio_app/) | Web UI for the semantic search engine | Gradio, Python |
| [**foundry_tools/**](foundry_tools/) | Azure AI Language apps (sentiment analysis & translation) | Azure AI Text Analytics, Azure Translator, Gradio |
| [**azure_ml/**](azure_ml/) | Model training notebook on Azure ML | Azure ML SDK v2, Jupyter |

---

## Semantic Search Engine

A FastAPI-based semantic search engine that indexes a corpus of sentences and finds the most semantically similar ones using cosine similarity. The corpus is auto-populated from the AG News dataset at startup.

- **Model**: `all-MiniLM-L6-v2` (configurable)
- **Endpoints**: similarity scoring, corpus management, semantic search
- **Deployment**: Dockerised for container hosting (e.g. Azure Container Apps)

```bash
cd search_engine
pip install -e .
uvicorn main:app --reload --port 3000
```

A companion **Gradio UI** is available in [`search_engine/gradio_app/`](search_engine/gradio_app/) for interactive use.

See the full [Search Engine README](search_engine/README.md) for API details, configuration, and Docker instructions.

---

## Azure AI Foundry Tools

Interactive Gradio web apps and CLI scripts for **Azure AI Language** services:

| Tool | Capability |
|------|------------|
| **Sentiment Analysis** | Analyse text sentiment with optional opinion mining, colour-coded results and confidence scores |
| **Translation** | Translate text between 16+ languages using the Azure Translator API |

```bash
cd foundry_tools
uv sync
uv run main.py          # launches tabbed Gradio UI at http://127.0.0.1:7860
```

### Required environment variables

```bash
# Sentiment Analysis (Azure AI Language)
export LANGUAGE_KEY="<your-key>"
export LANGUAGE_ENDPOINT="<your-endpoint>"

# Translation (Azure Translator)
export TRANSLATOR_TEXT_SUBSCRIPTION_KEY="<your-key>"
export TRANSLATOR_TEXT_ENDPOINT="<your-endpoint>"
export TRANSLATOR_TEXT_LOCATION="<your-region>"
```

See the full [Foundry Tools README](foundry_tools/README.md) for CLI usage and Azure deployment commands.

---

## Azure ML — Model Training

A Jupyter notebook ([`azure_ml/train_model.ipynb`](azure_ml/train_model.ipynb)) that demonstrates training a model inside an **Azure ML workspace**:

1. Authenticates via `DefaultAzureCredential`
2. Uploads a credit-card default dataset as a registered data asset
3. Trains and evaluates a model using Azure ML SDK v2

```bash
cd azure_ml
uv sync
# Open train_model.ipynb in VS Code or Jupyter
```

---

## Prerequisites

- **Python 3.12+**
- [**uv**](https://docs.astral.sh/uv/) package manager (recommended) or pip
- **Docker** (for containerised deployments)
- An **Azure subscription** with the following resources as needed:
  - Azure AI Language (for sentiment analysis)
  - Azure Translator (for translation)
  - Azure ML workspace (for model training)

## Repository Structure

```
ml-deployment-azure/
├── azure_ml/                   # Azure ML model training notebook
│   ├── train_model.ipynb
│   └── pyproject.toml
├── foundry_tools/              # Azure AI Language apps (Gradio + CLI)
│   ├── main.py                 # Multi-tab Gradio entry point
│   ├── sentiment_analysis_app/ # Sentiment analysis module
│   └── translation_app/        # Translation module
├── search_engine/              # Semantic search API
│   ├── main.py                 # FastAPI entry point
│   ├── Dockerfile
│   ├── src/search_engine/      # Core library (config, embeddings, index)
│   └── gradio_app/             # Gradio web UI for search
├── LICENSE                     # Apache 2.0
└── README.md
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).