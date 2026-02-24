import os
import azure.ai.translation.text as TextTranslation
from azure.core.credentials import AzureKeyCredential


TRANSLATOR_KEY = os.getenv("TRANSLATOR_TEXT_SUBSCRIPTION_KEY")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_TEXT_ENDPOINT")
TRANSLATOR_LOCATION = os.getenv("TRANSLATOR_TEXT_LOCATION") 

def authenticate_client():
    """Authenticate the Text Translation client using key and endpoint."""
    ta_credential = AzureKeyCredential(TRANSLATOR_KEY)
    return TextTranslation.TextTranslationClient(
        credential=ta_credential,
        region=TRANSLATOR_LOCATION
    )

if __name__ == "__main__":
    client = authenticate_client()

    # Sample text to translate
    text_to_translate = "I would really like to drive your car around the block a few times!"

    # Call the API to translate the text from English to French and German
    response = client.translate(
        body=[text_to_translate],
        from_language="en",
        to_language=["fr", "de"]
    )
    print("Translation response:")
    print(response)
    print(type(response))
    
    print("\n\nFirst item in response:")
    print(type(response[0]))
    print(response[0].translations)

    print("\n\nFirst translation:")
    print(response[0].translations[0].text)
    print(response[0].translations[0].to)

    print("\n\nAll translations:")
    # Print the translation results
    for translation in response:
        for t in translation.translations:
            print(f"Translated to {t.to}: {t.text}")