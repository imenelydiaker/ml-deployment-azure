import requests
import uuid
import json
import os

# Add your key and endpoint
key = os.getenv("TRANSLATOR_TEXT_SUBSCRIPTION_KEY")
endpoint = os.getenv("TRANSLATOR_TEXT_ENDPOINT")
location = os.getenv("TRANSLATOR_TEXT_LOCATION") # location, also known as region.

path = "/translate"
api_url = endpoint + path

params = {"api-version": "3.0", "from": "en", "to": ["fr", "de"]}

headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Ocp-Apim-Subscription-Region": location,
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4()),
}

# You can pass more than one object in body.
body = [{"text": "I would really like to drive your car around the block a few times!"}]

request = requests.post(api_url, params=params, headers=headers, json=body)
response = request.json()

print(
    json.dumps(
        response, sort_keys=True, ensure_ascii=False, indent=4, separators=(",", ": ")
    )
)
