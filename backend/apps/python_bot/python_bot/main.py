"""Simple example FastAPI app to demonstrate moonrepo inter-project dependencies."""

import logging

from chatwoot_api import GreetingRequest, GreetingResponse, greet
from fastapi import FastAPI

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/greet")
def greet_endpoint(request: GreetingRequest) -> GreetingResponse:
    """Use the chatwoot_api shared package to greet someone."""
    return greet(request)
