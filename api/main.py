"""
Phase 3 backend skeleton.

The only job of this file right now is to prove the deploy chain works:
frontend (GitHub Pages) -> this API (Render) -> a response back in the browser.
Nothing here talks to a database or a model yet — that's Phase 4 and 5.

Run locally with:
    pip install -r requirements.txt
    uvicorn main:app --reload
Then open http://127.0.0.1:8000/docs for the free interactive API tester.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sebastian Young — Portfolio API")

# CORS: without this, a browser on syoungcode.github.io calling this API
# (running on a different domain, onrender.com) gets silently blocked.
# Add any other origins you test from (e.g. a local dev server) to this list.
ALLOWED_ORIGINS = [
    "https://syoungcode.github.io",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/ping")
def ping():
    """The one throwaway endpoint for Phase 3 — just confirms the API is up."""
    return {"status": "ok", "message": "Backend is alive."}


@app.get("/")
def root():
    return {"message": "See /docs for the interactive API explorer."}
