import httpx
from fastapi import HTTPException

from tracker.logging_config import get_logger, setup_logging
from tracker.settings import settings

# Get logger for this module
logger = get_logger(__name__)


class EvalTrackClient:
    def get_traces(self) -> list[dict]:
        """Get traces from the eval-track service.

        Returns:
            dict: The traces data from the service.

        Raises:
            HTTPException: If the request fails or returns a non-200 status code.
        """
        url = f"{settings.eval_tracker_host}/traces"
        try:
            with httpx.Client() as client:
                ret = client.get(url)
                if ret.status_code != httpx.codes.OK:
                    error_msg = f"Failed to get traces: status code {ret.status_code}"
                    logger.error(error_msg, extra={"status_code": ret.status_code})
                    raise HTTPException(status_code=ret.status_code, detail=error_msg)
                logger.info("Successfully retrieved traces")
                return ret.json()
        except httpx.RequestError as exc:
            error_msg = f"Failed to connect to eval-track service: {exc}"
            logger.error(error_msg, extra={"error_type": type(exc).__name__})
            raise HTTPException(status_code=503, detail="Service temporarily unavailable")
        except Exception as exc:
            error_msg = f"Unexpected error while getting traces: {exc}"
            logger.error(error_msg, extra={"error_type": type(exc).__name__})
            raise HTTPException(status_code=500, detail="Internal server error")

    def put_trace(self, trace_id: str, data: dict) -> None:
        """Put a trace to the eval-track service.

        Args:
            trace_id: The ID of the trace to store.
            data: The trace data to store.

        Raises:
            HTTPException: If the request fails or returns a non-200 status code.
        """
        url = f"{settings.eval_tracker_host}/traces/{trace_id}"
        try:
            with httpx.Client() as client:
                ret = client.put(url, json=data)
                if ret.status_code != httpx.codes.OK:
                    error_msg = f"Failed to put trace: status code {ret.status_code}"
                    logger.error(error_msg, extra={"trace_id": trace_id, "status_code": ret.status_code})
                    raise HTTPException(status_code=ret.status_code, detail=error_msg)
                logger.info("Successfully stored trace", extra={"trace_id": trace_id})
        except httpx.RequestError as exc:
            error_msg = f"Failed to connect to eval-track service: {exc}"
            logger.error(error_msg, extra={"trace_id": trace_id, "error_type": type(exc).__name__})
            raise HTTPException(status_code=503, detail="Service temporarily unavailable")
        except Exception as exc:
            error_msg = f"Unexpected error while putting trace: {exc}"
            logger.error(error_msg, extra={"trace_id": trace_id, "error_type": type(exc).__name__})
            raise HTTPException(status_code=500, detail="Internal server error")
