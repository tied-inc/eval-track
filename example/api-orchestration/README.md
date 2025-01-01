# [Example]: API Orchestration

This example demonstrates how to use eval-track across multiple microservices. It showcases how to track communication between services using the EvalTrackClient and capture_response decorator.

## How to Run

```bash
git clone https://github.com/tied-inc/eval-track
cd example/api-orchestration
uv sync --frozen
uv main:app
```

## Endpoints

This application includes the following endpoints:

### eval-track Base Endpoints
- `GET /eval-track/health`
- `GET /eval-track/traces`
- `PUT /eval-track/traces/{trace_id}`

### Service Endpoints
- `GET /service1` - First microservice demo
- `GET /service2` - Second microservice demo
- `GET /orchestrate` - Service orchestration demo

## Features

1. **Microservices** (`/service1`, `/service2`)
   - Simulation of independent services
   - Example of asynchronous processing
   - Trace capture using @capture_response decorator

2. **Orchestration** (`/orchestrate`)
   - Parallel service calls
   - Error handling
   - Trace aggregation and display

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
   # Test individual services
   curl http://localhost:8000/service1
   curl http://localhost:8000/service2

   # Test orchestration
   curl http://localhost:8000/orchestrate
   ```

4. View traces:
   ```bash
   curl http://localhost:8000/eval-track/traces
   ```

## Implementation Details

This example demonstrates the following features:

1. **Using EvalTrackClient**
   - Retrieving and storing trace data
   - Aggregating traces from multiple services

2. **@capture_response Decorator**
   - Capturing traces in asynchronous functions
   - Trace capture during error conditions

3. **Inter-service Communication**
   - Asynchronous HTTP communication using httpx
   - Handling parallel requests
   - Error handling and recovery

For detailed implementation, please refer to [main.py](./main.py).
