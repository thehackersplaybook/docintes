# main.py
import logging
import os

from fastapi import FastAPI

from app.api import convert  # Import the routes from convert.py
from app.ratelimit.rlmiddleware import RateLimitMiddleware

app = FastAPI(title="File Converter API")

app.add_middleware(RateLimitMiddleware, max_requests=5, period=60)

# Include the router from the convert module
app.include_router(convert.router)
# Apply the ratelimit with a limit of 10 requests per minute
logging.info("Adding Middleware")
# Add the RateLimitMiddleware with desired max_requests and period


# Only include the test router in test mode

if os.getenv("TEST_ENV", "false").lower() == "true":
    app.include_router(convert.test_router)
