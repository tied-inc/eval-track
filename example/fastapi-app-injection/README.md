# [Example]: fastapi app injection

This example shows how you use this library for your own fastapi applications.

## Check it out

```bash
git clone https://github.com/tied-inc/eval-track
cd example
uv sync --frozen
uv main:app
```

This app contains below paths just including router from package

- `GET /eval-track/health`
- `GET /eval-track/traces`
- `PUT /eval-track/traces/{trace_id}`

## Description

This usage pattern is folowing below steps

1. install and import `eval-track/tracker` into your project
1. import router from `tracker/router`, then include it into your app



see more detail, [main.py](./main.py)