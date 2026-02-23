from pydantic import BaseModel


class Sentences(BaseModel):
    sentence1: str
    sentence2: str