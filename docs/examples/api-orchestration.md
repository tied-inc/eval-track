# API Orchestration Example

This example demonstrates how to use eval-track for tracing and monitoring distributed API calls across multiple microservices.

## Overview

The API Orchestration example shows how to implement trace collection and monitoring in a microservices architecture, with parallel request processing and comprehensive trace aggregation.

## Installation

### Prerequisites
- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- [Task](https://taskfile.dev/) (optional, for development tasks)

### Install using uv
```bash
# Clone the repository
git clone https://github.com/tied-inc/eval-track

# Navigate to the example directory
cd example/api-orchestration

# Install dependencies
uv sync --frozen
```

### Install using Task (recommended for development)
```bash
# Install Task if not already installed
npm install -g @go-task/cli

# Install uv if not already installed
task setup-uv

# Install dependencies
task install-tracker
```

### Running the Application
```bash
uv main:app
```

## Available Endpoints

This application includes the following endpoints:

### Basic eval-track Endpoints
- `GET /eval-track/health` - Health check endpoint
- `GET /eval-track/traces` - Retrieve all traces
- `PUT /eval-track/traces/{trace_id}` - Store trace data

### Service Endpoints
- `GET /service1` - First microservice demo
- `GET /service2` - Second microservice demo
- `GET /orchestrate` - Service orchestration demo

## Implementation Details

This example demonstrates:

1. **EvalTrackClient Usage**
   - Trace data retrieval and storage
   - Trace aggregation from multiple services

2. **@capture_response Decorator**
   - Async function tracing
   - Error state capture

3. **Inter-service Communication**
   - Async HTTP communication with httpx
   - Parallel request processing
   - Error handling and recovery

## Implementation

Here's how to implement API orchestration with eval-track:

```python
from fastapi import FastAPI, HTTPException
from tracker.tracer import capture_response
from tracker.client import EvalTrackClient
from pydantic import BaseModel
import httpx
import asyncio
from typing import List, Dict

class ServiceResponse(BaseModel):
    service: str
    status: str
    message: str

class OrchestrationResponse(BaseModel):
    services: List[ServiceResponse]
    total_time: float
    success_count: int

app = FastAPI()
client = EvalTrackClient()

@app.get("/service1")
@capture_response
async def service1() -> ServiceResponse:
    # Simulated service processing
    await asyncio.sleep(1)
    return ServiceResponse(
        service="service1",
        status="success",
        message="Service 1 processed successfully"
    )

@app.get("/service2")
@capture_response
async def service2() -> ServiceResponse:
    # Simulated service processing
    await asyncio.sleep(0.5)
    return ServiceResponse(
        service="service2",
        status="success",
        message="Service 2 processed successfully"
    )

@app.get("/orchestrate")
@capture_response
async def orchestrate() -> OrchestrationResponse:
    async with httpx.AsyncClient() as client:
        # Make parallel requests to services
        tasks = [
            client.get("http://localhost:8000/service1"),
            client.get("http://localhost:8000/service2")
        ]

        start_time = time.time()
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.time() - start_time

        # Process responses
        services = []
        success_count = 0

        for response in responses:
            if isinstance(response, Exception):
                services.append(
                    ServiceResponse(
                        service="unknown",
                        status="error",
                        message=str(response)
                    )
                )
            else:
                service_data = response.json()
                services.append(ServiceResponse(**service_data))
                if service_data["status"] == "success":
                    success_count += 1

        return OrchestrationResponse(
            services=services,
            total_time=total_time,
            success_count=success_count
        )
```

## Features Demonstrated

### 1. Parallel Request Processing
- Asynchronous HTTP requests using `httpx`
- Concurrent service calls with `asyncio.gather`
- Response time tracking

### 2. Error Handling
- Exception handling for failed requests
- Service status tracking
- Aggregated error reporting

### 3. Trace Aggregation
- Individual service traces
- Orchestration-level tracing
- Performance metrics collection

## Trace Data Collection

The `@capture_response` decorator captures:
- Individual service responses
- Orchestration metadata
- Timing information
- Error states

## Advanced Usage Patterns

### Service Health Monitoring
```python
@app.get("/health")
@capture_response
async def check_health() -> Dict[str, str]:
    services = await get_service_health()
    return {
        "orchestrator": "healthy",
        "services": services
    }
```

### Circuit Breaking Pattern
```python
@capture_response
async def call_with_circuit_breaker(service_url: str) -> ServiceResponse:
    if await is_circuit_open(service_url):
        return ServiceResponse(
            service=service_url,
            status="error",
            message="Circuit breaker open"
        )
    return await make_service_call(service_url)
```

## Best Practices

1. Implement proper timeout handling
2. Use circuit breakers for resilience
3. Track service health metrics
4. Implement proper error handling
5. Use structured logging

For more information about trace collection and monitoring, see the [Client documentation](../client.md).
