# eval-track

## Overview
`eval-track` is a series of LLM-ML observability and tracking services. This series provides APIs for retrieving and storing trace data.

## Contents

- [eval-track/tracker](./tracker/): Python tracker library for FastAPI
- [Documentation](./docs/): Project documentation using MkDocs

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

4. Run tests:
    ```sh
    task test-tracker
    ```

5. Format code:
    ```sh
    task check-all-tracker
    ```
