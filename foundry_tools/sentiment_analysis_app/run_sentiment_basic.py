"""
Sentiment Analysis WITHOUT opinion mining.

This script analyses documents for overall and per-sentence sentiment
but does not extract granular target/assessment opinions.
"""

import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

LANGUAGE_KEY = os.getenv('LANGUAGE_KEY')
LANGUAGE_ENDPOINT = os.getenv('LANGUAGE_ENDPOINT')


def authenticate_client():
    """Authenticate the Text Analytics client using key and endpoint."""
    ta_credential = AzureKeyCredential(LANGUAGE_KEY)
    return TextAnalyticsClient(
        endpoint=LANGUAGE_ENDPOINT,
        credential=ta_credential
    )


def print_separator(char="=", length=70):
    print(char * length)


if __name__ == "__main__":
    client = authenticate_client()

    # Sample documents for basic sentiment analysis (no opinion mining)
    documents = [
        "I had an average experience at the restaurant. Nothing special, but nothing bad either.",
        "The new software update is amazing! It fixed all the bugs and the interface is much smoother now.",
        "The delivery was late, the packaging was damaged, and the product inside was broken. Never ordering again.",
    ]

    # Call the API WITHOUT opinion mining
    result = client.analyze_sentiment(documents, show_opinion_mining=False)
    doc_results = [doc for doc in result if not doc.is_error]

    # Summary counts
    positive_reviews = [doc for doc in doc_results if doc.sentiment == "positive"]
    negative_reviews = [doc for doc in doc_results if doc.sentiment == "negative"]
    mixed_reviews = [doc for doc in doc_results if doc.sentiment == "mixed"]
    neutral_reviews = [doc for doc in doc_results if doc.sentiment == "neutral"]

    print_separator("*")
    print("  SENTIMENT ANALYSIS (BASIC — NO OPINION MINING)")
    print_separator("*")
    print(f"\n  Total documents analysed : {len(doc_results)}")
    print(f"  Positive : {len(positive_reviews)}  |  Negative : {len(negative_reviews)}  "
          f"|  Mixed : {len(mixed_reviews)}  |  Neutral : {len(neutral_reviews)}\n")

    for idx, document in enumerate(doc_results):
        print_separator()
        print(f"  Document #{idx + 1}")
        print_separator()
        print(f"  Overall Sentiment : {document.sentiment.upper()}")
        print(f"  Confidence Scores : positive={document.confidence_scores.positive:.2f}  "
              f"neutral={document.confidence_scores.neutral:.2f}  "
              f"negative={document.confidence_scores.negative:.2f}")
        print_separator("-")

        for s_idx, sentence in enumerate(document.sentences):
            print(f"\n  Sentence {s_idx + 1}: \"{sentence.text}\"")
            print(f"    Sentiment : {sentence.sentiment}")
            print(f"    Scores    : positive={sentence.confidence_scores.positive:.2f}  "
                  f"neutral={sentence.confidence_scores.neutral:.2f}  "
                  f"negative={sentence.confidence_scores.negative:.2f}")

        print()

    print_separator("*")
    print("  Done.")
    print_separator("*")
