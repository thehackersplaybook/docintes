# main.py
from fastapi import FastAPI
from app.api import convert  # Import the routes from convert.py
from app.ratelimit.rlmiddleware import RateLimitMiddleware
import logging

app = FastAPI(title="File Converter API")

# Include the router from the convert module
app.include_router(convert.router)
# Apply the ratelimit with a limit of 10 requests per minute
logging.info("Adding Middleware")
# Add the RateLimitMiddleware with desired max_requests and period
app.add_middleware(RateLimitMiddleware, max_requests=5, period=60)
