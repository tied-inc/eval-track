import logging

import httpx

from tracker.settings import settings

logger = logging.getLogger(__name__)


class EvalTrackClient:
    def get_traces(self) -> dict:
        url = f"{settings.eval_tracker_host}/traces"
        try:
            with httpx.Client() as client:
                ret = client.get(url)
                if ret.status_code != httpx.codes.OK:
                    logger.error(f"receive not ok status code: {ret.status_code}")
                logger.info("get traces succeeded")
                return ret.json()
        except Exception:
            logger.error("receive unexpected error")
            return {}

    def put_trace(self, trace_id: str, data: dict) -> None:
        url = f"{settings.eval_tracker_host}/traces/{trace_id}"
        try:
            with httpx.Client() as client:
                ret = client.put(url, data=data)
                if ret.status_code != httpx.codes.OK:
                    logger.error(f"receive not ok status code: {ret.status_code}")
                logger.info("put trace succeeded")
        except Exception:
            logger.error("receive unexpected error")
