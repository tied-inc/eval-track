# Tracer Module

The tracer module provides functionality for capturing responses from functions across multiple languages:

- Python: Using the `capture_response` decorator in `tracer.py`
- Go: Using the `CaptureResponse` function in the `client` package
- TypeScript: Using the `captureResponse` function

## Go Usage

### Installation

#### Prerequisites
- Go version 1.20 or higher
- Working Go environment (GOPATH configured)
- [Task](https://taskfile.dev/) (optional, for development tasks)

#### Install using go get
```bash
go get github.com/tied-inc/eval-track/tracker-go
```

#### Install using Task (recommended for development)
```bash
# Install Task if not already installed
npm install -g @go-task/cli

# Install dependencies
task install-tracker
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

## TypeScript Usage

### Installation

#### Prerequisites
- Node.js version 18 or higher
- pnpm (recommended), npm, or yarn
- [Task](https://taskfile.dev/) (optional, for development tasks)

#### Install using package manager
```bash
# Using pnpm (recommended)
pnpm install @tied-inc/eval-track

# Or using npm
npm install @tied-inc/eval-track

# Or using yarn
yarn add @tied-inc/eval-track
```

#### Install using Task (recommended for development)
```bash
# Install Task if not already installed
npm install -g @go-task/cli

# Install dependencies
task install-tracker
```

### Basic Usage

```typescript
import { captureResponse } from '@tied-inc/eval-track';

// Define your response type
interface Response {
  message: string;
}

// Basic async function
async function getData(): Promise<Response> {
  return { message: "Hello from TypeScript!" };
}

// Wrap the function
const wrappedFn = captureResponse(getData);

// Use the wrapped function
const result = await wrappedFn();
console.log(result.message);
```

### Error Handling

```typescript
import { z } from 'zod';
import { captureResponse } from '@tied-inc/eval-track';

// Define schema for validation
const ResponseSchema = z.object({
  data: z.string(),
  timestamp: z.number(),
});

type Response = z.infer<typeof ResponseSchema>;

// Function that might throw
async function riskyOperation(): Promise<Response> {
  throw new Error('Operation failed');
}

// Errors are captured in trace data
const wrapped = captureResponse(riskyOperation);
try {
  await wrapped();
} catch (error) {
  console.error(error);
}
```

### Features

- Generates unique trace IDs using ULID
- Uses Zod for runtime type validation
- Supports both synchronous and asynchronous functions
- Preserves function signatures using TypeScript types
- Automatically serializes responses to JSON

### Internal Operation

1. When `captureResponse` is called, it creates a closure that wraps the original function
2. Each function call generates a unique trace ID using ULID
3. The wrapped function executes the original function inside a try-catch block
4. Response data or error is captured and sent to the trace server asynchronously
5. The original return value or error is passed through unchanged

### Limitations

- Return values should be JSON-serializable objects
- Error objects are stringified for trace storage
- Trace data storage is asynchronous and may not complete immediately
- Network errors during trace storage are logged but don't affect the wrapped function

For more detailed information and advanced usage examples, see the [TypeScript tracer README](../tracker-ts/README.md).

## Go Internal Operation

1. When `CaptureResponse` is called, it uses reflection to analyze the function signature
2. A new function is created that matches the original signature exactly
3. Each function call generates a unique trace ID using ULID
4. The wrapped function executes the original function and captures its return values
5. Response data or error is sent to the trace server asynchronously
6. Original return values are passed through unchanged

### Go Limitations

- Functions must return (T, error) where T is any type
- Return values must be JSON-serializable
- Reflection usage may impact performance on very hot code paths
- Trace data storage is asynchronous and may not complete immediately
- Network errors during trace storage are logged but don't affect the wrapped function

For more detailed information and advanced usage examples, see the [Go tracer README](../tracker-go/README.md).

## Rust Usage

### Installation

#### Prerequisites
- Rust with Cargo installed
- [Task](https://taskfile.dev/) (optional, for development tasks)

#### Install using Cargo
```bash
cargo add eval-track-rust --git https://github.com/tied-inc/eval-track
```

#### Install using Task (recommended for development)
```bash
# Install Task if not already installed
npm install -g @go-task/cli

# Install dependencies
task install-tracker
```

### Basic Usage

```rust
use tracker::{capture_response, init_tracer};

// Initialize the tracer
init_tracer("http://localhost:8000");

// Define your response type
#[derive(serde::Serialize, serde::Deserialize)]
struct Response {
    message: String,
}

// Use the capture_response attribute
#[capture_response]
fn get_data() -> Response {
    Response {
        message: String::from("Hello from Rust!")
    }
}

// Async function support
#[capture_response]
async fn get_data_async() -> Response {
    Response {
        message: String::from("Hello from async Rust!")
    }
}
```

### Error Handling

```rust
use tracker::{capture_response, TracerError};

#[capture_response]
fn risky_operation() -> Result<Response, TracerError> {
    if some_condition {
        Err(TracerError::OperationFailed("Operation failed".into()))
    } else {
        Ok(Response {
            message: String::from("Success!")
        })
    }
}
```

### Features

- Generates unique trace IDs using ULID
- Supports both synchronous and asynchronous functions via procedural macro
- Uses thiserror for robust error handling
- Thread-safe global tracer client
- Automatic serialization using serde
- Support for Result types and custom errors

### Internal Operation

1. The `capture_response` procedural macro generates wrapper code at compile time
2. Each function call generates a unique trace ID using ULID
3. The function is executed and its return value or error is captured
4. Trace data is sent to the server asynchronously
5. Original return value or error is passed through unchanged

### Limitations

- Return values must implement serde::Serialize
- Error types must implement std::error::Error
- Trace data storage is asynchronous and may not complete immediately
- Network errors during trace storage are logged but don't affect the wrapped function

For more detailed information and advanced usage examples, see the [Rust tracer README](../tracker-rs/README.md).

## Python Usage

### Installation

#### Prerequisites
- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- [Task](https://taskfile.dev/) (optional, for development tasks)

#### Install using uv
```bash
uv pip install "git+https://github.com/tied-inc/eval-track/tracker"
```

#### Install using Task (recommended for development)
```bash
# Install Task if not already installed
npm install -g @go-task/cli

# Install uv if not already installed
task setup-uv

# Install dependencies
task install-tracker
```

### capture_response Decorator

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
