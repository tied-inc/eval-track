# Rust Tracer

A Rust implementation of the eval-track tracer with support for both synchronous and asynchronous functions.

## Features

- Function response capture using procedural macros
- Support for both sync and async functions
- Automatic ULID generation for trace IDs
- JSON request/response capture
- Error handling and propagation
- Thread-safe global tracer client
- Compatible with other language implementations

## Installation

### Prerequisites
- Rust with Cargo installed
- [Task](https://taskfile.dev/) (optional, for development tasks)

### Install using Cargo
Add the following to your `Cargo.toml`:

```toml
[dependencies]
tracker = { git = "https://github.com/tied-inc/eval-track", package = "tracker" }
```

### Install using Task (recommended for development)
```bash
# Install Task if not already installed
npm install -g @go-task/cli

# Install dependencies
task install-tracker
```

## Usage

### Basic Usage

```rust
use tracker::{init_tracer, capture_response};

// Initialize the tracer with your API endpoint
init_tracer("https://api.example.com");

// Use the capture_response attribute macro
#[capture_response]
fn my_function(x: i32) -> Result<i32, String> {
    Ok(x * 2)
}

// The function will automatically capture traces
let result = my_function(21)?;
assert_eq!(result, 42);
```

### Async Functions

```rust
use tracker::{init_tracer, capture_response};

#[capture_response]
async fn async_function(input: String) -> Result<String, String> {
    Ok(input.to_uppercase())
}

#[tokio::main]
async fn main() -> Result<(), String> {
    init_tracer("https://api.example.com");

    let result = async_function("hello".to_string()).await?;
    assert_eq!(result, "HELLO");
    Ok(())
}
```

### Error Handling

The tracer automatically captures both successful responses and errors:

```rust
#[capture_response]
fn failing_function() -> Result<(), String> {
    Err("something went wrong".to_string())
}

let result = failing_function();
assert!(result.is_err());
```

### Manual Client Usage

If you need more control, you can use the `TracerClient` directly:

```rust
use tracker::{TracerClient, Trace};
use serde_json::json;
use chrono::Utc;
use ulid::Ulid;

async fn manual_trace() -> Result<(), Box<dyn std::error::Error>> {
    let client = TracerClient::new("https://api.example.com");

    let trace = Trace {
        id: Ulid::new().to_string(),
        request: json!({ "method": "GET", "path": "/api/data" }),
        response: json!({ "status": 200, "data": "success" }),
        created_at: Utc::now(),
        updated_at: Utc::now(),
    };

    client.put_trace(&trace).await?;
    Ok(())
}
```

## Development

### Running Tests

```bash
# Run unit tests
cargo test

# Run integration tests
cargo test --features integration-tests

# Run all tests with coverage
cargo test --all-features
```

### Project Structure

- `src/`: Core implementation
  - `lib.rs`: Main library interface
  - `client.rs`: HTTP client implementation
  - `types.rs`: Data structures
  - `error.rs`: Error types
- `capture-response-macro/`: Procedural macro implementation
- `tests/`: Test suite
  - `client_test.rs`: Client tests
  - `decorator_test.rs`: Macro tests
  - `integration_test.rs`: Integration tests
