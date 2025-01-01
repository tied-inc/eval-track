# Tracer Module

`tracer.py` defines the `capture_response` decorator for capturing responses from functions and coroutines.


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
