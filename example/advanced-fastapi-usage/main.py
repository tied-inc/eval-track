from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tracker.router import router
from tracker.tracer import capture_response
from uvicorn import run


class ResponseModel(BaseModel):
    message: str
    details: dict | None = None


class CalculationResponse(BaseModel):
    result: float
    operation: str


app = FastAPI()
app.include_router(router)


@capture_response
@app.get("/hello")
def hello_endpoint() -> ResponseModel:
    """Basic endpoint demonstrating trace capture with sync function."""
    return ResponseModel(
        message="Hello from eval-track!", details={"timestamp": "2024-01-01T00:00:00Z"}
    )


@capture_response
@app.get("/async-calc/{x}/{y}")
async def async_calculation(x: float, y: float) -> CalculationResponse:
    """Async endpoint demonstrating trace capture with calculation."""
    if y == 0:
        raise HTTPException(status_code=400, detail="Division by zero not allowed")

    result = x / y
    return CalculationResponse(result=result, operation=f"Division of {x} by {y}")


@capture_response
@app.get("/error-demo")
def error_endpoint() -> ResponseModel:
    """Endpoint demonstrating trace capture with error handling."""
    raise HTTPException(
        status_code=400,
        detail="This is a demonstration error that will be captured in traces",
    )


def main() -> None:
    """Run the FastAPI application."""
    run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
