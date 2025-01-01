# Router Module

`router.py` defines the API endpoints for trace data.

## API Endpoints

### GET /eval-track/health
Health check endpoint.


**Response**:
- `200 OK`: When the service is operating normally
- Response body: `"OK"`

### GET /eval-track/traces
Endpoint for retrieving trace data.

**Response**:
- `200 OK`: When trace data is successfully retrieved
- Response body: `{"message": "Logs endpoint"}`

### PUT /eval-track/traces/{trace_id}
Endpoint for storing trace data.

**Path Parameters**:
- `trace_id` (str): Unique identifier for the trace

**Request Body**:
- `data` (dict): Trace data to store

**Response**:
- `204 No Content`: When trace data is successfully stored
- Response body: None

## Logging

Each endpoint outputs the following logs:

- Health check: "Health check endpoint called"
- Trace retrieval: "Logs retrieval endpoint called"
- Trace storage: "Received logs with traceId: {trace_id}"

## Configuration

- Router prefix is set to `/eval-track`
- Logging is configured using NullHandler
