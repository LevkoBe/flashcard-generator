from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.api import test_sets, test_cards, scores
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

app.include_router(test_sets.router, prefix="/api", tags=["test-sets"])
app.include_router(test_cards.router, prefix="/api", tags=["test-cards"])
app.include_router(scores.router, prefix="/api", tags=["scores"])


@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")
