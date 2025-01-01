# FastAPI Injection Example

This example demonstrates how to integrate the eval-track router directly into your FastAPI application for observability and trace management.

## Overview

The FastAPI injection example shows the simplest way to add eval-track's tracing capabilities to your FastAPI application by including the provided router.

## Setup

```bash
# Clone the repository
git clone https://github.com/tied-inc/eval-track

# Navigate to the example directory
cd example

# Install dependencies
uv sync --frozen

cd fastapi-app-injection

# Run the application
uv main:app
```

## Implementation

Here's how to inject the eval-track router into your FastAPI application:

```python
from fastapi import FastAPI
from tracker.router import router
from uvicorn import run

def main() -> None:
    app = FastAPI()
    # Include the eval-track router in your FastAPI application
    app.include_router(router)

    run(app)
```

## Available Endpoints

After including the router, your application will have access to the following endpoints:

- `GET /eval-track/health`
  - Health check endpoint for the eval-track service

- `GET /eval-track/traces`
  - Retrieve all stored traces

- `PUT /eval-track/traces/{trace_id}`
  - Store trace data for a specific trace ID

## Usage Pattern

The implementation follows these steps:

1. Install the eval-track package in your project
2. Import the router from `tracker.router`
3. Include the router in your FastAPI application using `app.include_router()`

This pattern allows you to:
- Monitor API endpoints automatically
- Collect trace data for observability
- Access trace management endpoints

## Error Handling

The included router handles common error cases:
- Invalid trace IDs
- Missing or malformed trace data
- Authentication failures

For detailed error responses, refer to the [Router documentation](../router.md).
