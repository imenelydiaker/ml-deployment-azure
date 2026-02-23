# Tranlsation App

## Deployment on Azure

Either use the portal (recommended) or the CLI with the following command:

```sh
az cognitiveservices account create \
  --name <translator-name> \
  --resource-group <resource-group> \
  --kind TextTranslation \
  --sku F0 \ # Free tier, up to 2M characters
  --location <region> \ # eastus, francecentral, westus, etc.
  --yes
```


## Usage

Install uv if not installed yet from [here](https://docs.astral.sh/uv/getting-started/installation/). Then export the following environment variables:

```sh
export TRANSLATOR_TEXT_SUBSCRIPTION_KEY="..."
export TRANSLATOR_TEXT_ENDPOINT="..."
export TRANSLATOR_TEXT_LOCATION="..."
```

Now run the script to use the API:

```sh
uv run run_translations.py
```

## Request Format

**POST** `{endpoint}/translate`

**Query Parameters:**

| Parameter     | Value   | Description                          |
|---------------|---------|--------------------------------------|
| `api-version` | `3.0`   | API version                          |
| `from`        | `en`    | Source language code                  |
| `to`          | `fr,zu` | Target language code(s), repeatable  |

**Headers:**

| Header                          | Description                                      |
|---------------------------------|--------------------------------------------------|
| `Ocp-Apim-Subscription-Key`    | Your Translator resource subscription key        |
| `Ocp-Apim-Subscription-Region` | Region of your Translator resource               |
| `Content-Type`                  | `application/json`                               |
| `X-ClientTraceId`              | A unique GUID to identify the request (optional) |

**Request Body:**

An array of objects, each with a `text` field containing the string to translate:

```json
[{"text": "I would really like to drive your car around the block a few times!"}]
```

## Response Format

```json
[
    {
        "translations": [
            {
                "text": "J’aimerais vraiment faire le tour du pâté de maisons avec ta voiture !",
                "to": "fr"
            },
            {
                "text": "Ngingathanda ukushayela imoto yakho ezungeze ibhlokhi izikhathi ezimbalwa!",
                "to": "zu"
            }
        ]
    }
]
```
