from fastapi import FastAPI
from pydantic import BaseModel
from tracker.router import router
from tracker.decorator import capture_response
from tracker.client import EvalTrackClient
from uvicorn import run
import httpx
from httpx import Response
import asyncio


class ServiceResponse(BaseModel):
    service_name: str
    message: str
    status: str


class OrchestrationResponse(BaseModel):
    request_id: str
    services: list[ServiceResponse]
    summary: str


app = FastAPI()
app.include_router(router)
client = EvalTrackClient()


@capture_response
@app.get("/service1")
async def service1() -> ServiceResponse:
    """First microservice endpoint."""
    await asyncio.sleep(0.1)  # Simulate processing
    return ServiceResponse(
        service_name="service1", message="Service 1 processed request", status="success"
    )


@capture_response
@app.get("/service2")
async def service2() -> ServiceResponse:
    """Second microservice endpoint."""
    await asyncio.sleep(0.2)  # Simulate processing
    return ServiceResponse(
        service_name="service2", message="Service 2 processed request", status="success"
    )


@capture_response
@app.get("/orchestrate")
async def orchestrate() -> OrchestrationResponse:
    """Orchestrates calls to multiple services and tracks their responses."""
    async with httpx.AsyncClient() as http_client:
        # Parallel service calls
        tasks = [
            http_client.get("http://localhost:8000/service1"),
            http_client.get("http://localhost:8000/service2"),
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        services = []
        for i, response in enumerate(responses):
            service_name = f"service{i+1}"
            if isinstance(response, Response):
                try:
                    data = response.json()
                    services.append(ServiceResponse(**data))
                except Exception as e:
                    services.append(
                        ServiceResponse(
                            service_name=service_name,
                            message=f"Failed to parse response: {str(e)}",
                            status="error",
                        )
                    )
            else:
                error_message = (
                    str(response)
                    if isinstance(response, Exception)
                    else "Unknown error"
                )
                services.append(
                    ServiceResponse(
                        service_name=service_name, message=error_message, status="error"
                    )
                )

        # Get all traces for demonstration
        traces = client.get_traces()

        return OrchestrationResponse(
            request_id="demo-123",
            services=services,
            summary=f"Orchestrated {len(services)} services. Traces collected: {len(traces)}",
        )


def main() -> None:
    """Run the FastAPI application."""
    run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
