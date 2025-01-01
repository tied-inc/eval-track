import time
from typing import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from tracker.logging_config import get_logger, setup_logging
from tracker.settings import settings

# Ensure logging is configured
setup_logging()

# Get logger for this module
logger = get_logger(__name__)


async def error_handling_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Global error handling middleware.

    Catches any unhandled exceptions in the request processing pipeline and ensures
    they are properly logged and returned as JSON responses.

    Args:
        request: The incoming HTTP request
        call_next: The next middleware or route handler in the chain

    Returns:
        Response: Either the normal response or a JSON error response
    """
    try:
        return await call_next(request)
    except Exception as exc:
        error_msg = f"Unhandled error processing request: {exc}"
        logger.error(
            error_msg, extra={"error_type": type(exc).__name__, "path": request.url.path, "method": request.method}
        )
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})


async def secret_key_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Middleware that adds the secret key to the request headers.

    This middleware is responsible for adding the secret key to the request headers
    before passing the request to the next middleware in the chain. The secret key is
    retrieved from the settings object.

    Args:
        request (Request): The incoming request object.
        call_next (Callable[[Request], Awaitable[Response]]): The next middleware in the chain.

    Returns:
        Response: The response object returned by the next middleware in the chain.
    """
    # Skip auth for health check endpoint
    if request.url.path == "/eval-track/health":
        return await call_next(request)

    header_key = request.headers.get("x-eval-tracker-secret-key")
    expected_key = settings.eval_tracker_secret_key.get_secret_value()

    # Skip auth if no secret key is configured (development/test environment)
    if not expected_key:
        return await call_next(request)

    # Both missing key and invalid key should return the same error
    # to avoid information leakage
    if not header_key or header_key != expected_key:
        logger.error("Invalid secret key", extra={"header_key": "REDACTED"})
        return JSONResponse(content={"detail": "Invalid secret key"}, status_code=403)

    response = await call_next(request)

    return response


async def api_access_log_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """
    Middleware to log details of incoming HTTP requests and their responses.
    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable[[Request], Awaitable[Response]]): The next middleware or route handler to be called.
    Returns:
        Response: The HTTP response generated by the next middleware or route handler.
    Logs:
        - When a request is received, logs the HTTP method, path, and query parameters.
        - If the client disconnects before the response is sent, logs a disconnection message.
        - When a request is processed, logs the HTTP method, path, query parameters,
            status code, and elapsed time in seconds.
    """
    start_time = time.perf_counter()
    logger.info(
        "Request received",
        extra={
            "method": request.method,
            "path": request.url.path,
            "query": str(request.query_params),
        },
    )
    response = await call_next(request)
    if await request.is_disconnected():
        logger.info("Client disconnected before sending the response.")

    elapsed_time = time.perf_counter() - start_time
    logger.info(
        "Request processed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "query": str(request.query_params),
            "status_code": response.status_code,
            "elapsed_time_sec": round(elapsed_time, 3),
        },
    )
    return response
