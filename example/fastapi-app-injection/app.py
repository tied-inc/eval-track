from fastapi import FastAPI
from tracker.router import router
from uvicorn import run


def main() -> None:
    app = FastAPI()
    app.include_router(router)

    run(app)

if __name__ == "__main__":
    main()