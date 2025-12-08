from fastapi import APIRouter

router = APIRouter()

@router.get("/evaluate/{name}")
def evaluate(name: str):
    return {"template": name, "score": 50, "winner": False, "action": "pause"}
