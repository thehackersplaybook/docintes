import os

import pytest

from app.api.convert import test_router
from fastapi import FastAPI, Request, HTTPException
from app.main import app
from httpx import ASGITransport
from httpx import AsyncClient
from app.ratelimit.rlmiddleware import RateLimitMiddleware


@pytest.mark.asyncio
async def test_rate_limit():
    transport = ASGITransport(app=app)  # Use ASGITransport to wrap the FastAPI app
    app.router = test_router
    app.add_middleware(RateLimitMiddleware, max_requests=5, period=60)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        for _ in range(5):
            response = await client.get("/test-only")
            assert response.status_code == 200

        # Make one more request to exceed the rate limit
        with pytest.raises(HTTPException):
            response = await client.get("/test-only")
