# Sentiment Analysis App

Analyse the sentiment of text documents using the **Azure AI Language – Text Analytics** API.  
Two scripts are provided:

| Script | Opinion Mining | Description |
|--------|:-:|-------------|
| `run_sentiment_analysis.py` | Yes | Returns document/sentence sentiment **plus** granular target & assessment opinions. |
| `run_sentiment_basic.py` | No | Returns document/sentence sentiment only (faster, lower cost). |
| `sentiment_analysis_app.py` | Toggle | Interactive **Gradio** web UI with an opinion-mining checkbox. |

---

## Prerequisites

- **Python 3.12+**
- [**uv**](https://docs.astral.sh/uv/) package manager (or pip)
- An **Azure AI Language** resource (the *Language* service in the Azure portal)
- Copy the **Key** and **Endpoint** from the resource's *Keys and Endpoint* page.

---

## Environment Setup


### Deployment on Azure

Either use the portal (recommended) or the CLI with the following command:

```sh
az cognitiveservices account create \
  --name <translator-name> \
  --resource-group <resource-group> \
  --kind TextAnalytics \
  --sku F0 \ # Free tier, up to 2M characters
  --location <region> \ # eastus, francecentral, westus, etc.
  --yes
```

### 1. Install dependencies

From the `foundry_tools/` project root:

```bash
uv sync          # installs everything from pyproject.toml
```

### 2. Set environment variables

```bash
export LANGUAGE_KEY="<your-language-resource-key>"
export LANGUAGE_ENDPOINT="<your-language-resource-endpoint>"
```

> The endpoint looks like `https://<resource-name>.cognitiveservices.azure.com/`.

---

## Running the Scripts

```bash
# With opinion mining
uv run sentiment_analysis_app/run_sentiment_analysis.py

# Without opinion mining (basic)
uv run sentiment_analysis_app/run_sentiment_basic.py
```

### Running the Gradio Web App

```bash
uv run sentiment_analysis_app/sentiment_analysis_app.py
```

This launches a local web server (default `http://127.0.0.1:7860`).  
In the UI you can:

- **Enter text** — paste one or more documents. Separate multiple documents with a **blank line**.
- **Toggle opinion mining** — check/uncheck the *Enable opinion mining* checkbox.
- **Use examples** — click any pre-built example at the bottom of the page.

Results are displayed as rich HTML with colour-coded sentiment badges and confidence-score bars.

---

## API Input Format

Both scripts call `TextAnalyticsClient.analyze_sentiment()`.  
The input is a **list of plain-text strings** (documents), for example:

```python
documents = [
    "The food and service were unacceptable. The concierge was nice, however.",
    "The rooms were beautiful and the staff was incredibly helpful.",
]
```

**Limits (per request):**

| Constraint | Value |
|------------|-------|
| Maximum documents per request | 10 |
| Maximum characters per document | 5,120 |
| Maximum total size per request | 1 MB |

---

## API Output Format

### Basic sentiment (no opinion mining)

For each document the API returns:

```
document
├── sentiment          : "positive" | "negative" | "neutral" | "mixed"
├── confidence_scores
│   ├── positive       : 0.00 – 1.00
│   ├── neutral        : 0.00 – 1.00
│   └── negative       : 0.00 – 1.00
└── sentences[]
    ├── text           : the sentence string
    ├── sentiment      : "positive" | "negative" | "neutral"
    └── confidence_scores
        ├── positive   : 0.00 – 1.00
        ├── neutral    : 0.00 – 1.00
        └── negative   : 0.00 – 1.00
```

### With opinion mining (`show_opinion_mining=True`)

Each sentence additionally contains **mined opinions** that break down sentiment into specific **targets** (nouns/aspects) and **assessments** (adjectives/descriptors):

```
sentence
└── mined_opinions[]
    ├── target
    │   ├── text             : e.g. "food"
    │   ├── sentiment        : "positive" | "negative" | "mixed"
    │   └── confidence_scores
    │       ├── positive     : 0.00 – 1.00
    │       └── negative     : 0.00 – 1.00
    └── assessments[]
        ├── text             : e.g. "unacceptable"
        ├── sentiment        : "positive" | "negative"
        └── confidence_scores
            ├── positive     : 0.00 – 1.00
            └── negative     : 0.00 – 1.00
```

### Example console output (with opinion mining)

```
**********************************************************************
  SENTIMENT ANALYSIS WITH OPINION MINING
**********************************************************************

  Total documents analysed : 3
  Positive : 1  |  Negative : 1  |  Mixed : 1  |  Neutral : 0

======================================================================
  Document #1
======================================================================
  Overall Sentiment : MIXED
  Confidence Scores : positive=0.47  neutral=0.00  negative=0.53
----------------------------------------------------------------------

  Sentence 1: "The food and service were unacceptable."
    Sentiment : negative
    Scores    : positive=0.00  neutral=0.00  negative=1.00

      Target: "food"  ->  negative
        Scores: positive=0.00  negative=1.00
        Assessment: "unacceptable"  ->  negative
          Scores: positive=0.00  negative=1.00
```

---

## Resources

- [Azure AI Language documentation](https://learn.microsoft.com/azure/ai-services/language-service/)
- [Sentiment analysis & opinion mining overview](https://learn.microsoft.com/azure/ai-services/language-service/sentiment-opinion-mining/overview)
- [Python SDK reference – `azure-ai-textanalytics`](https://learn.microsoft.com/python/api/azure-ai-textanalytics/)