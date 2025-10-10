from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import test_sets, test_cards, scores

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_sets.router, prefix="/api", tags=["test-sets"])
app.include_router(test_cards.router, prefix="/api", tags=["test-cards"])
app.include_router(scores.router, prefix="/api", tags=["scores"])


@app.get("/")
def read_root():
    return {"Welcome": "Flashcard Generator"}
