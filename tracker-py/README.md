# eval-track/tracker

This library is LLM-ML observability tool for Python.

## Usage

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

**usage example**

- [fastapi-app-injection](../example/fastapi-app-injection/)
    - show and describe how you use this library inside your FastAPI app

### Docker

1. authenticating with your personal access token
    - https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic
2. pull images from registry

```bash
echo {YOUR_TOKEN} | docker login ghcr.io -u USERNAME --password-stdin
docker pull ghcr.io/tied-inc/eval-track:latest
```
