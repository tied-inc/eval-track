# [Example]: Advanced FastAPI Usage

This example demonstrates advanced usage patterns for eval-track. It includes practical implementations of asynchronous processing, error handling, and trace functionality.

## How to Run

```bash
git clone https://github.com/tied-inc/eval-track
cd example/advanced-fastapi-usage
uv sync --frozen
uv main:app
```

## Endpoints

This application includes the following endpoints:

### eval-track Base Endpoints
- `GET /eval-track/health`
- `GET /eval-track/traces`
- `PUT /eval-track/traces/{trace_id}`

### Sample Endpoints
- `GET /hello` - Basic trace functionality demo
- `GET /async-calc/{x}/{y}` - Asynchronous processing and calculation demo
- `GET /error-demo` - Error handling demo

## Features

1. **Basic Trace Functionality** (`/hello`)
   - Trace capture in synchronous functions
   - Response using Pydantic models

2. **Asynchronous Calculation** (`/async-calc/{x}/{y}`)
   - Trace capture in asynchronous functions
   - Error handling (division by zero)
   - Path parameter usage example

3. **Error Handling** (`/error-demo`)
   - HTTPException demonstration
   - Trace capture during errors

## Usage

1. Install eval-track:
   ```bash
   uv pip install "git+https://github.com/tied-inc/eval-track/tracker"
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Test the endpoints:
   ```bash
   # Basic trace
   curl http://localhost:8000/hello

   # Asynchronous calculation
   curl http://localhost:8000/async-calc/10/2

   # Error handling
   curl http://localhost:8000/error-demo
   ```

4. View traces:
   ```bash
   curl http://localhost:8000/eval-track/traces
   ```

For detailed implementation, please refer to [main.py](./main.py).
