from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/evaluate/{name}")
def evaluate(name: str):
    score = random.randint(10, 200)
    return {
        "template": name,
        "score": score,
        "winner": score > 120,
        "action": "scale" if score > 120 else "pause"
    }
