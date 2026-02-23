from sentence_transformers import SentenceTransformer, util


class Model:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def predict(self, sentence1: str, sentence2: str) -> float:
        encoded_sentence1 = self.model.encode(sentence1)
        encoded_sentence2 = self.model.encode(sentence2)
        sim_score = util.cos_sim(encoded_sentence1, encoded_sentence2)
        return float(sim_score.numpy()[0][0])