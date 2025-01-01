import pytest
from fastapi import FastAPI, HTTPException
from httpx import ASGITransport, AsyncClient

from app.api.convert import test_router
from app.ratelimit.rlmiddleware import RateLimitMiddleware


@pytest.mark.asyncio
async def test_rate_limit():
    test_app = FastAPI()
    test_app.add_middleware(RateLimitMiddleware, max_requests=5, period=60)
    transport = ASGITransport(app=test_app)  # Use ASGITransport to wrap the FastAPI app
    test_app.router = test_router
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        for _ in range(5):
            response = await client.get("/test-only")
            assert response.status_code == 200

        # Make one more request to exceed the rate limit
        with pytest.raises(HTTPException):
            response = await client.get("/test-only")
