from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

api = FastAPI()

fb_bart_large_mnli = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    multi_label=True
)

ml_mdeberta_v3_xnli = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7",
    multi_label=True
)

ml_deberta_v3_zeroshot = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0",
    multi_label=True
)


class TextData(BaseModel):
    text: str
    words: list[str]
    model: str


@api.post("/process_text/")
async def process_text(data: TextData):
    if data.model == 'facebook/bart-large-mnli':
        return zero_shot(fb_bart_large_mnli, data.text, data.words)
    elif data.model == 'MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7':
        return zero_shot(ml_mdeberta_v3_xnli, data.text, data.words)
    elif data.model == 'MoritzLaurer/deberta-v3-large-zeroshot-v2.0':
        return zero_shot(ml_deberta_v3_zeroshot, data.text, data.words)


def zero_shot(model, text: str, words: list[str]):
    return model(text, candidate_labels=words)
