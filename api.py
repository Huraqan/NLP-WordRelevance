from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

api = FastAPI()

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    multi_label=True
)


class TextData(BaseModel):
    text: str
    words: list[str]


@api.post("/process_text/")
async def process_text(data: TextData):
    return zero_shot(data.text, data.words)


def zero_shot(text: str, words: list[str]):
    return classifier(text, candidate_labels=words)
