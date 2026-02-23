# Foundry Tools

A collection of Azure AI Language applications with both CLI scripts and an interactive **Gradio** web UI.

## Project Structure

```
foundry_tools/
├── main.py                          # Multi-page Gradio app (entry point)
├── pyproject.toml                   # Project config & dependencies
├── sentiment_analysis_app/
│   ├── run_sentiment_analysis.py    # CLI – sentiment with opinion mining
│   ├── run_sentiment_basic.py       # CLI – sentiment without opinion mining
│   ├── sentiment_analysis_app.py    # Gradio interface for sentiment analysis
│   └── README.md                    # Detailed docs for the sentiment app
└── translation_app/
    ├── run_translations.py          # CLI – translation script
    ├── translation_app.py           # Gradio interface for translation
    └── README.md                    # Detailed docs for the translation app
```

## Prerequisites

- **Python 3.12+**
- [**uv**](https://docs.astral.sh/uv/) package manager

## Environment Setup

### 1. Install dependencies

```bash
cd foundry_tools
uv sync
```

### 2. Set environment variables

**Sentiment Analysis** (Azure AI Language):

```bash
export LANGUAGE_KEY="<your-language-resource-key>"
export LANGUAGE_ENDPOINT="<your-language-resource-endpoint>"
```

**Translation** (Azure Translator):

```bash
export TRANSLATOR_TEXT_SUBSCRIPTION_KEY="<your-translator-key>"
export TRANSLATOR_TEXT_ENDPOINT="<your-translator-endpoint>"
export TRANSLATOR_TEXT_LOCATION="<your-translator-region>"
```

## Running the Gradio App

Launch the multi-page web UI that combines both tools under a single tabbed interface:

```bash
uv run main.py
```

This starts a local server at `http://127.0.0.1:7860` with two tabs:

| Tab | Description |
|-----|-------------|
| **Sentiment Analysis** | Analyse text sentiment with optional opinion mining. Colour-coded badges and confidence bars. |
| **Translation** | Translate text between 16+ languages using the Azure Translator API. |

You can also run each app individually:

```bash
uv run sentiment_analysis_app/sentiment_analysis_app.py
uv run translation_app/translation_app.py
```

## Running the CLI Scripts

```bash
# Sentiment analysis with opinion mining
uv run sentiment_analysis_app/run_sentiment_analysis.py

# Sentiment analysis without opinion mining
uv run sentiment_analysis_app/run_sentiment_basic.py

# Translation
uv run translation_app/run_translations.py
```
