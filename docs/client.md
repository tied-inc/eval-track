# Client Module

`client.py` defines the `EvalTrackClient` class for trace operations.

## EvalTrackClient Class

A client class for retrieving and storing trace data.

### Methods

#### get_traces()
Retrieves trace data.

**Returns**:
- `dict`: Retrieved trace data
  - Returns an empty dictionary `{}` on error

**Example**:
```python
from tracker.client import EvalTrackClient

client = EvalTrackClient()
traces = client.get_traces()
```

#### put_trace(trace_id: str, data: dict)
Stores trace data.

**Parameters**:
- `trace_id` (str): Unique identifier for the trace
- `data` (dict): Trace data to store

**Returns**:
- `None`

**Example**:
```python
from tracker.client import EvalTrackClient

client = EvalTrackClient()
client.put_trace("trace-123", {"request": "...", "response": "..."})
```

### Error Handling
- Outputs error logs when HTTP requests fail (status code other than 200)
- Outputs error logs for unexpected errors
