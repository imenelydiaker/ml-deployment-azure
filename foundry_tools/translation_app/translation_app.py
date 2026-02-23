import gradio as gr
import requests
import uuid
import json
import os

# Azure Translator configuration
TRANSLATOR_API_KEY = os.getenv("TRANSLATOR_TEXT_SUBSCRIPTION_KEY")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_TEXT_ENDPOINT")
TRANSLATOR_LOCATION = os.getenv("TRANSLATOR_TEXT_LOCATION")

LANGUAGES = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Chinese (Simplified)": "zh-Hans",
    "Chinese (Traditional)": "zh-Hant",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Hindi": "hi",
    "Russian": "ru",
    "Dutch": "nl",
    "Swedish": "sv",
    "Turkish": "tr",
    "Zulu": "zu",
}


def translate(text: str, source_language: str, target_language: str) -> str:
    """Translate text using Azure Translator API."""
    if not text.strip():
        return ""

    if not all([TRANSLATOR_API_KEY, TRANSLATOR_ENDPOINT, TRANSLATOR_LOCATION]):
        return "Error: Missing Azure Translator credentials. Set TRANSLATOR_TEXT_SUBSCRIPTION_KEY, TRANSLATOR_TEXT_ENDPOINT, and TRANSLATOR_TEXT_LOCATION environment variables."

    source_code = LANGUAGES.get(source_language, "en")
    target_code = LANGUAGES.get(target_language, "fr")

    path = "/translate"
    constructed_url = TRANSLATOR_ENDPOINT + path

    params = {
        "api-version": "3.0",
        "from": source_code,
        "to": [target_code],
    }

    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_API_KEY,
        "Ocp-Apim-Subscription-Region": TRANSLATOR_LOCATION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": text}]

    try:
        response = requests.post(
            constructed_url, params=params, headers=headers, json=body
        )
        response.raise_for_status()
        result = response.json()
        translated_text = result[0]["translations"][0]["text"]
        return translated_text
    except requests.exceptions.RequestException as e:
        return f"Translation error: {e}"
    except (KeyError, IndexError):
        return f"Unexpected response format: {json.dumps(result, indent=2)}"


# Add English to the source language choices
source_languages = ["English"] + list(LANGUAGES.keys())
target_languages = list(LANGUAGES.keys())

demo = gr.Interface(
    fn=translate,
    inputs=[
        gr.Textbox(label="Text to translate", lines=5, placeholder="Enter text here..."),
        gr.Dropdown(choices=source_languages, value="English", label="Source Language"),
        gr.Dropdown(choices=target_languages, value="French", label="Target Language"),
    ],
    outputs=gr.Textbox(label="Translated text", lines=5),
    title="Azure Translator",
    description="Translate text between languages using the Azure Translator API.",
    flagging_mode="never",
    examples=[
        ["Hello, how are you today?", "English", "French"],
        ["I would like to order a coffee, please.", "English", "Spanish"],
        ["The weather is beautiful this morning.", "English", "German"],
    ],
)

if __name__ == "__main__":
    demo.launch(
        theme=gr.themes.Soft()
    )
