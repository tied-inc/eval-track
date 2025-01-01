# eval-track/tracker

This library is LLM-ML observability tool for Python.

## Usage

### Package installation

```bash
uv pip install "git+https://github.com/tied-inc/eval-track/tracker"
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