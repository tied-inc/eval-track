# eval-track Documentation

`eval-track` is a library that provides observability and tracking services for LLM-ML. This documentation explains the usage and functionality of the main components.

## Main Components

### [Client](client.md)
Client class for retrieving and storing trace data.

### [Tracer](tracer.md)
Decorator for capturing function and coroutine responses.

### [Router](router.md)
API endpoints for trace data.

## Installation

```bash
uv pip install "git+https://github.com/tied-inc/eval-track/tracker"
```

For detailed usage instructions, please refer to each component's documentation.

## Examples

The following examples demonstrate different ways to integrate and use eval-track in your applications:

### [Advanced FastAPI Usage](examples/advanced-fastapi-usage.md)
Demonstrates advanced patterns including async processing, error handling, and Pydantic model integration.

### [API Orchestration](examples/api-orchestration.md)
Illustrates microservice orchestration with parallel request processing and comprehensive trace aggregation.

Each example includes detailed setup instructions, implementation details, and best practices for using eval-track in different scenarios.
