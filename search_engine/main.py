import sys
import logging
import json
from fastapi import FastAPI

from search_engine.models import Sentences
from search_engine.similarity_model import Model

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Initialize model when the app starts
logging.info("Load model from sentence-transformers")
model = Model()

# Initialize app
logging.info("Start API")
app = FastAPI()


@app.get("/")
def home():
    return {"Server message": "Welcome to sentence similarity computing API !"}


@app.post("/similarity")
def similarity(sentences: Sentences):
    """Compute similarity between 2 sentences

    Args:
        sentences (Sentences): a dict of 2 sentences, keys are 'sentence1' and 'sentence2'

    Returns:
        dict[str, float]: similarity score returned as a dict {'sim_score': a number}
    """
    score = model.predict(sentence1=sentences.sentence1, sentence2=sentences.sentence2)
    logging.info(f"Predicted similarity: {round(score, 2)}")
    return json.dumps({"sim_score": str(score)})