"""Simple example package to demonstrate moonrepo inter-project dependencies."""

import logging

from pydantic import BaseModel

from chatwoot_api.settings import settings

logger = logging.getLogger(__name__)

__all__ = [
    "GreetingRequest",
    "GreetingResponse",
    "greet",
    "settings",
]


class GreetingRequest(BaseModel):
    name: str


class GreetingResponse(BaseModel):
    message: str


def greet(request: GreetingRequest) -> GreetingResponse:
    """Return a greeting for the given name."""
    logger.info("Greeting %s", request.name)
    return GreetingResponse(message=f"Hello, {request.name}!")
