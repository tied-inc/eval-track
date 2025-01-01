# Tracer Module

The tracer module provides functionality for capturing responses from functions across multiple languages:

- Python: Using the `capture_response` decorator in `tracer.py`
- Go: Using the `CaptureResponse` function in the `client` package
- TypeScript: Using the `captureResponse` function

## Go Usage

### Installation

```bash
go get github.com/tied-inc/eval-track/tracker-go
```

### Basic Usage

```go
package main

import (
    "github.com/tied-inc/eval-track/tracker-go/pkg/client"
)

// Define your response struct
type Response struct {
    Message string `json:"message"`
}

func main() {
    // Create a new tracer client
    tracer := client.NewTracerClient("http://localhost:8000")

    // Wrap a function that returns (Response, error)
    wrappedFn := tracer.CaptureResponse(func() (Response, error) {
        return Response{Message: "Hello"}, nil
    })

    // Call the wrapped function
    response, err := wrappedFn()
    if err != nil {
        // Handle error
    }
}
```

### Error Handling

```go
// Function that may return an error
wrappedFn := tracer.CaptureResponse(func(x int) (Response, error) {
    if x < 0 {
        return Response{}, fmt.Errorf("negative input: %d", x)
    }
    return Response{Message: fmt.Sprintf("Input: %d", x)}, nil
})

// The error will be captured in the trace data
response, err := wrappedFn(-1)
```

### Features

- Generates unique trace IDs using ULID
- Supports both successful responses and errors
- Preserves function signatures using Go's reflection
- Automatically serializes responses to JSON
- Thread-safe client implementation

## Python Usage

## capture_response Decorator

A decorator that automatically records function return values as trace data. Supports both synchronous and asynchronous functions.

### Usage

```python
from tracker.tracer import capture_response
from pydantic import BaseModel

class Response(BaseModel):
    message: str

@capture_response
async def async_function() -> Response:
    return Response(message="Hello")

@capture_response
def sync_function() -> Response:
    return Response(message="World")
```

### Features

- Generates unique trace IDs using ULID
- Uses FastAPI's BackgroundTasks for asynchronous trace data storage
- Function return values must be Pydantic BaseModel instances
- Original function signatures and attributes are preserved using @wraps

### Internal Operation

1. When the decorator is applied, a unique trace ID is generated
2. The function is executed and its return value is captured
3. Trace data is stored asynchronously using BackgroundTasks
4. The original return value is passed through unchanged

### Supported Function Types

- Synchronous functions (defined with `def`)
- Asynchronous functions (defined with `async def`)

### Limitations

- Return values must be instances of classes that inherit from Pydantic's BaseModel
- Trace data storage is asynchronous and may not complete immediately
