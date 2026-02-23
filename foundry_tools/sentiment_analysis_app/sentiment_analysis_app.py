import os
import gradio as gr
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

LANGUAGE_KEY = os.getenv("LANGUAGE_KEY")
LANGUAGE_ENDPOINT = os.getenv("LANGUAGE_ENDPOINT")

SENTIMENT_COLORS = {
    "positive": "#22c55e",
    "negative": "#ef4444",
    "neutral": "#a3a3a3",
    "mixed": "#f59e0b",
}


def authenticate_client():
    """Authenticate the Text Analytics client."""
    ta_credential = AzureKeyCredential(LANGUAGE_KEY)
    return TextAnalyticsClient(
        endpoint=LANGUAGE_ENDPOINT,
        credential=ta_credential,
    )


def _badge(sentiment: str) -> str:
    """Return an HTML badge for a sentiment label."""
    color = SENTIMENT_COLORS.get(sentiment, "#6b7280")
    return (
        f'<span style="background:{color};color:#fff;padding:2px 10px;'
        f'border-radius:12px;font-size:0.85em;font-weight:600;">'
        f"{sentiment.upper()}</span>"
    )


def _score_bar(label: str, value: float, color: str) -> str:
    """Return an HTML progress-bar snippet for a confidence score."""
    pct = value * 100
    return (
        f'<div style="display:flex;align-items:center;gap:6px;margin:2px 0;">'
        f'<span style="width:70px;font-size:0.82em;color:#555;">{label}</span>'
        f'<div style="flex:1;background:#e5e7eb;border-radius:6px;height:14px;">'
        f'<div style="width:{pct:.1f}%;background:{color};height:100%;border-radius:6px;"></div>'
        f"</div>"
        f'<span style="width:42px;font-size:0.82em;text-align:right;">{value:.2f}</span>'
        f"</div>"
    )


def analyse_sentiment(text: str, opinion_mining: bool) -> str:
    """Call Azure Text Analytics and return formatted HTML results."""
    if not text.strip():
        return '<p style="color:#888;">Please enter some text.</p>'

    if not all([LANGUAGE_KEY, LANGUAGE_ENDPOINT]):
        return (
            '<p style="color:#ef4444;">Error: Set <code>LANGUAGE_KEY</code> and '
            "<code>LANGUAGE_ENDPOINT</code> environment variables.</p>"
        )

    client = authenticate_client()

    # Split on double-newlines so users can submit multiple documents
    documents = [d.strip() for d in text.split("\n\n") if d.strip()]

    try:
        results = client.analyze_sentiment(
            documents, show_opinion_mining=opinion_mining
        )
    except Exception as e:
        return f'<p style="color:#ef4444;">API error: {e}</p>'

    doc_results = [doc for doc in results if not doc.is_error]
    errors = [doc for doc in results if doc.is_error]

    if not doc_results and errors:
        return '<p style="color:#ef4444;">All documents returned errors.</p>'

    # ---- Build HTML output ----
    counts = {s: sum(1 for d in doc_results if d.sentiment == s)
              for s in ("positive", "negative", "neutral", "mixed")}

    html_parts = [
        '<div style="font-family:system-ui,sans-serif;">',
        '<h3 style="margin-bottom:4px;">Summary</h3>',
        "<p>" + "  &nbsp;|&nbsp;  ".join(
            f"{_badge(s)} {counts[s]}" for s in ("positive", "negative", "neutral", "mixed")
        ) + "</p>",
    ]

    for idx, doc in enumerate(doc_results):
        html_parts.append(
            '<div style="border:1px solid #e5e7eb;border-radius:10px;'
            'padding:16px;margin-bottom:14px;">'
        )
        html_parts.append(
            f"<h4>Document #{idx + 1} &nbsp; {_badge(doc.sentiment)}</h4>"
        )
        html_parts.append(_score_bar("Positive", doc.confidence_scores.positive, "#22c55e"))
        html_parts.append(_score_bar("Neutral", doc.confidence_scores.neutral, "#a3a3a3"))
        html_parts.append(_score_bar("Negative", doc.confidence_scores.negative, "#ef4444"))

        for s_idx, sentence in enumerate(doc.sentences):
            html_parts.append(
                '<div style="margin-top:10px;padding:10px;background:#f9fafb;'
                'border-radius:8px;">'
            )
            html_parts.append(
                f'<p style="margin:0 0 4px 0;"><strong>Sentence {s_idx + 1}:</strong> '
                f'"{sentence.text}" &nbsp; {_badge(sentence.sentiment)}</p>'
            )
            html_parts.append(_score_bar("Positive", sentence.confidence_scores.positive, "#22c55e"))
            html_parts.append(_score_bar("Neutral", sentence.confidence_scores.neutral, "#a3a3a3"))
            html_parts.append(_score_bar("Negative", sentence.confidence_scores.negative, "#ef4444"))

            if opinion_mining and sentence.mined_opinions:
                html_parts.append(
                    '<div style="margin-top:8px;padding-left:12px;'
                    'border-left:3px solid #d1d5db;">'
                )
                for opinion in sentence.mined_opinions:
                    target = opinion.target
                    html_parts.append(
                        f'<p style="margin:4px 0;font-size:0.9em;">'
                        f'<strong>Target:</strong> "{target.text}" &nbsp; '
                        f"{_badge(target.sentiment)}</p>"
                    )
                    for assessment in opinion.assessments:
                        html_parts.append(
                            f'<p style="margin:2px 0 2px 16px;font-size:0.85em;">'
                            f'Assessment: "{assessment.text}" &nbsp; '
                            f"{_badge(assessment.sentiment)}</p>"
                        )
                html_parts.append("</div>")

            html_parts.append("</div>")  # sentence card

        html_parts.append("</div>")  # document card

    html_parts.append("</div>")
    return "\n".join(html_parts)


# ---- Gradio UI ----
demo = gr.Interface(
    fn=analyse_sentiment,
    inputs=[
        gr.Textbox(
            label="Text to analyse",
            lines=6,
            placeholder="Enter text here...\n\nSeparate multiple documents with a blank line.",
        ),
        gr.Checkbox(label="Enable opinion mining", value=True),
    ],
    outputs=gr.HTML(label="Results"),
    title="Azure Sentiment Analysis",
    description=(
        "Analyse the sentiment of text using the Azure AI Language API.  \n"
        "Toggle **opinion mining** to see granular target & assessment breakdowns.  \n"
        "Separate multiple documents with a **blank line**."
    ),
    flagging_mode="never",
    examples=[
        ["The food and service were unacceptable. The concierge was nice, however.", True],
        ["The rooms were beautiful and the staff was incredibly helpful. Best hotel experience ever!", True],
        [
            "The laptop has a fantastic display, but the battery life is disappointing.\n\n"
            "The delivery was late and the product was broken. Never ordering again.",
            True,
        ],
        ["I had an average experience at the restaurant. Nothing special, but nothing bad either.", False],
        ["The new software update is amazing! It fixed all the bugs and the interface is much smoother now.", False],
    ],
)

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
