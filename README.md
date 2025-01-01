# eval-track

## Overview
`eval-track` is a series of LLM-ML observability and tracking services. This series provides APIs for retrieving and storing trace data across multiple programming languages.

## Contents

- [eval-track/tracker-py](./tracker-py/): Python tracker library
- [eval-track/tracker-ts](./tracker-ts/): TypeScript tracker library
- [eval-track/tracker-go](./tracker-go/): Go tracker library
- [eval-track/tracker-rs](./tracker-rs/): Rust tracker library
- [Documentation](./docs/): Project documentation using MkDocs

## Development Setup

### Prerequisites

- Python 3.8+ with [uv](https://github.com/astral-sh/uv)
- Node.js 18+ with [pnpm](https://pnpm.io/)
- Go 1.20+
- Rust with Cargo
- [Task](https://taskfile.dev/) for running development commands

### Installation

1. Install Task (if not already installed):
    ```sh
    npm install -g @go-task/cli
    ```

2. Set up Python environment:
    ```sh
    task setup-uv  # if uv not installed
    task install-tracker
    ```

3. Install TypeScript dependencies:
    ```sh
    cd tracker-ts
    pnpm install
    ```

4. Install Go dependencies:
    ```sh
    cd tracker-go
    go mod download
    ```

5. Install Rust dependencies:
    ```sh
    cd tracker-rs
    cargo build
    ```

### Testing

Run tests for each implementation:

```sh
# Python tests
task test-tracker
uv run pytest tests/

# TypeScript tests
cd tracker-ts && pnpm test

# Go tests
cd tracker-go && go test ./...

# Rust tests
cd tracker-rs && cargo test
```

### Code Quality

Format and lint the code:

```sh
# Python
task check-all-tracker  # Runs ruff format, ruff check, and mypy

# TypeScript
cd tracker-ts && pnpm lint

# Go
cd tracker-go && go fmt ./... && go vet ./...

# Rust
cd tracker-rs && cargo fmt && cargo clippy
```

## Documentation

### Local Development
To view and develop the documentation locally:

1. Install MkDocs and the Material theme:
    ```sh
    pip install mkdocs mkdocs-material
    ```

2. Start the documentation server:
    ```sh
    mkdocs serve
    ```
    This will start a local server at http://127.0.0.1:8000

3. Build the documentation:
    ```sh
    mkdocs build
    ```
    This will create a `site` directory with the built documentation.

## Contributing
We welcome contributions to the `eval-track` project. To get started, follow these steps:

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd eval-track

    # optional
    # if task not installed
    # other installation is https://taskfile.dev/installation/
    npm install -g @go-task/cli
    task setup-uv # if uv not installed
    ```

2. Install the necessary dependencies:
    ```sh
    task install-tracker
    ```

3. Run the application:
    ```sh
    task start-tracker-app
    ```

4. Run code quality checks:
    ```bash
    task check-all-tracker  # Python checks
    cd tracker-ts && pnpm lint  # TypeScript checks
    cd tracker-go && go fmt ./... && go vet ./...  # Go checks
    cd tracker-rs && cargo fmt && cargo clippy  # Rust checks
    ```
