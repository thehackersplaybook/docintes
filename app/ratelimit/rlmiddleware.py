import logging
from time import time

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("middle_ware")


# Custom ratelimit for rate limiting
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, period: int):
        super().__init__(app)
        self.max_requests = max_requests  # Maximum number of requests
        self.period = period  # Time window in seconds
        self.clients = {}  # Store request timestamps for each client IP

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host  # Get the client's IP address
        current_time = time()  # Get the current time in seconds

        # Initialize or update request history for the client
        if client_ip not in self.clients:
            self.clients[client_ip] = []
        else:
            # Remove timestamps older than the rate limit period
            self.clients[client_ip] = [
                timestamp
                for timestamp in self.clients[client_ip]
                if current_time - timestamp < self.period
            ]

        # Check if the client has exceeded the rate limit
        if len(self.clients[client_ip]) >= self.max_requests:
            logger.info("Middleware coming into the play, too many requests")
            raise HTTPException(status_code=429, detail="Too Many Requests")

        # Add the current request timestamp
        self.clients[client_ip].append(current_time)

        # Proceed with the request
        logger.info("Proceeding with the request from middleware")
        return await call_next(request)
