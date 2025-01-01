# Advanced FastAPI Usage Example

This example demonstrates advanced usage patterns of eval-track with FastAPI, including asynchronous processing, error handling, and Pydantic model integration.

## Overview

The Advanced FastAPI Usage example showcases more sophisticated integration patterns with eval-track, demonstrating how to handle complex scenarios in production environments.

## Setup

```bash
# Clone the repository
git clone https://github.com/tied-inc/eval-track

# Navigate to the example directory
cd example

# Install dependencies
uv sync --frozen

cd advanced-fastapi-usage

# Run the application
uv main:app
```

## Available Endpoints

This application includes the following endpoints:

### Basic eval-track Endpoints
- `GET /eval-track/health` - Health check endpoint
- `GET /eval-track/traces` - Retrieve all traces
- `PUT /eval-track/traces/{trace_id}` - Store trace data

### Example Endpoints
- `GET /hello` - Basic trace functionality demo
- `GET /async-calc/{x}/{y}` - Async processing and calculation demo
- `GET /error-demo` - Error handling demonstration

## Implementation

Here's how to implement advanced eval-track features in your FastAPI application:

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from tracker.tracer import capture_response
from tracker.client import EvalTrackClient
from pydantic import BaseModel
from typing import List, Optional

class ProcessingRequest(BaseModel):
    text: str
    options: Optional[List[str]] = None

class ProcessingResponse(BaseModel):
    result: str
    processed_options: Optional[List[str]] = None

app = FastAPI()
client = EvalTrackClient()

@app.post("/process", response_model=ProcessingResponse)
@capture_response
async def process_text(request: ProcessingRequest, background_tasks: BackgroundTasks) -> ProcessingResponse:
    try:
        # Simulate async processing
        result = await process_text_async(request.text)

        # Handle options if provided
        processed_options = await process_options(request.options) if request.options else None

        response = ProcessingResponse(
            result=result,
            processed_options=processed_options
        )

        # Add background task for additional processing
        background_tasks.add_task(store_processing_result, response)

        return response
    except Exception as e:
        # Error handling with proper status codes
        raise HTTPException(status_code=500, detail=str(e))
```

## Features Demonstrated

### 1. Asynchronous Processing
- Use of `async/await` for non-blocking operations
- Integration with FastAPI's `BackgroundTasks`
- Parallel processing of options

### 2. Error Handling
- Custom exception handling with proper HTTP status codes
- Integration with eval-track's trace capture
- Graceful error reporting

### 3. Pydantic Model Integration
- Request/Response model validation
- Optional field handling
- Type safety with Python type hints

## Trace Data

The `@capture_response` decorator automatically captures:
- Request payload including text and options
- Response data with results
- Processing time and errors (if any)

## Advanced Usage Patterns

### Background Processing
```python
async def store_processing_result(response: ProcessingResponse) -> None:
    # Store results asynchronously
    await client.put_trace(
        trace_id=generate_trace_id(),
        data=response.dict()
    )
```

### Error Handling Pattern
```python
@capture_response
async def handle_with_fallback(request: ProcessingRequest) -> ProcessingResponse:
    try:
        result = await primary_processing(request)
    except Exception:
        # Fallback to secondary processing
        result = await secondary_processing(request)
    return result
```

## Best Practices

1. Always use Pydantic models for request/response handling
2. Implement proper error handling with specific status codes
3. Utilize background tasks for non-critical operations
4. Structure your code for maintainability and testing

For more details about error handling and router configuration, see the [Router documentation](../router.md).
