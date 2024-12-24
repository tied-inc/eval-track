from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from tracker.middleware import secret_key_middleware, api_access_log_middleware
from tracker.router import router
from tracker.settings import settings

app = FastAPI()
app.include_router(router)

app.middleware("http")(secret_key_middleware)
app.middleware("http")(api_access_log_middleware)
if settings.eval_tracker_trusted_hosts:
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=settings.eval_tracker_trusted_hosts
    )
