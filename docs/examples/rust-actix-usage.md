# Advanced Rust Usage with Actix Web

This example demonstrates how to use the eval-track Rust tracer with an Actix Web application, showing function response capture across multiple endpoints and middleware.

## Installation

### Prerequisites
- Rust with Cargo installed
- [Task](https://taskfile.dev/) (optional, for development tasks)

### Install using Cargo
Add the following to your `Cargo.toml`:
```toml
[dependencies]
eval-track-rust = { git = "https://github.com/tied-inc/eval-track" }
actix-web = "4"
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
```

### Install using Task (recommended for development)
```bash
# Install Task if not already installed
npm install -g @go-task/cli

# Install dependencies
task install-tracker
```

## Basic Actix Web Integration

```rust
use actix_web::{web, App, HttpResponse, HttpServer};
use tracker::{capture_response, init_tracer};
use serde::{Deserialize, Serialize};

// Define response types
#[derive(Serialize, Deserialize)]
struct ServiceResponse {
    message: String,
    timestamp: i64,
}

#[derive(Serialize, Deserialize)]
struct OrchestrationResponse {
    service1: ServiceResponse,
    service2: ServiceResponse,
    orchestrated_at: i64,
}

// Initialize tracer in main
#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Initialize tracer with your endpoint
    init_tracer("http://localhost:8000");

    HttpServer::new(|| {
        App::new()
            .service(web::resource("/service1").to(service1))
            .service(web::resource("/service2").to(service2))
            .service(web::resource("/orchestrate").to(orchestrate))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}

// Service endpoints
#[capture_response]
async fn service1() -> HttpResponse {
    let response = ServiceResponse {
        message: "Service 1 response".into(),
        timestamp: chrono::Utc::now().timestamp(),
    };
    HttpResponse::Ok().json(response)
}

#[capture_response]
async fn service2() -> HttpResponse {
    let response = ServiceResponse {
        message: "Service 2 response".into(),
        timestamp: chrono::Utc::now().timestamp(),
    };
    HttpResponse::Ok().json(response)
}

// Orchestration endpoint
#[capture_response]
async fn orchestrate() -> Result<HttpResponse, actix_web::Error> {
    let client = awc::Client::default();

    // Make parallel requests to services
    let (service1_resp, service2_resp) = tokio::join!(
        client.get("http://localhost:8080/service1").send(),
        client.get("http://localhost:8080/service2").send()
    );


    let service1_data: ServiceResponse = service1_resp?.json().await?;
    let service2_data: ServiceResponse = service2_resp?.json().await?;

    let response = OrchestrationResponse {
        service1: service1_data,
        service2: service2_data,
        orchestrated_at: chrono::Utc::now().timestamp(),
    };

    Ok(HttpResponse::Ok().json(response))
}
```

## Advanced Error Handling

```rust
use tracker::{TracerError, capture_response};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ServiceError {
    #[error("Service unavailable: {0}")]
    Unavailable(String),
    #[error("Invalid input: {0}")]
    InvalidInput(String),
    #[error(transparent)]
    Other(#[from] anyhow::Error),
}

impl From<ServiceError> for TracerError {
    fn from(err: ServiceError) -> Self {
        TracerError::OperationFailed(err.to_string())
    }
}

#[capture_response]
async fn risky_service() -> Result<ServiceResponse, ServiceError> {
    if rand::random::<f64>() > 0.5 {
        Err(ServiceError::Unavailable("Service temporarily down".into()))
    } else {
        Ok(ServiceResponse {
            message: "Service successful".into(),
            timestamp: chrono::Utc::now().timestamp(),
        })
    }
}
```

## Request Context Tracking

```rust
use std::future::{ready, Ready};
use actix_web::dev::{forward_ready, Service, ServiceRequest, ServiceResponse, Transform};
use futures_util::future::LocalBoxFuture;
use uuid::Uuid;

// Request context
#[derive(Clone, Debug)]
struct RequestContext {
    request_id: String,
    user_id: Option<String>,
    start_time: i64,
}

// Middleware for adding context
struct ContextMiddleware;

impl<S, B> Transform<S, ServiceRequest> for ContextMiddleware
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = actix_web::Error>,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = actix_web::Error;
    type Transform = ContextMiddlewareService<S>;
    type InitError = ();
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ready(Ok(ContextMiddlewareService { service }))
    }
}

struct ContextMiddlewareService<S> {
    service: S,
}

impl<S, B> Service<ServiceRequest> for ContextMiddlewareService<S>
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = actix_web::Error>,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = actix_web::Error;
    type Future = LocalBoxFuture<'static, Result<Self::Response, Self::Error>>;

    forward_ready!(service);

    fn call(&self, req: ServiceRequest) -> Self::Future {
        let context = RequestContext {
            request_id: Uuid::new_v4().to_string(),
            user_id: req.headers().get("X-User-ID")
                .and_then(|v| v.to_str().ok())
                .map(String::from),
            start_time: chrono::Utc::now().timestamp(),
        };

        req.extensions_mut().insert(context.clone());

        let fut = self.service.call(req);
        Box::pin(async move {
            let res = fut.await?;
            Ok(res)
        })
    }
}

// Usage with context
#[capture_response]
async fn contextual_service(req: HttpRequest) -> Result<HttpResponse, actix_web::Error> {
    let context = req.extensions()
        .get::<RequestContext>()
        .expect("Context not found");

    let response = ServiceResponse {
        message: format!("Request {} processed", context.request_id),
        timestamp: chrono::Utc::now().timestamp(),
    };

    Ok(HttpResponse::Ok().json(response))
}

// Register middleware in main
fn main() {
    HttpServer::new(|| {
        App::new()
            .wrap(ContextMiddleware)
            .service(web::resource("/contextual").to(contextual_service))
    })
}
```

This example demonstrates:
1. Basic Actix Web integration with traced endpoints
2. Request orchestration using tokio::join!
3. Advanced error handling with custom error types
4. Request context tracking and duration measurement
5. Middleware composition for tracing and context
6. Type safety with serde serialization

The tracer captures all responses and errors automatically, providing observability across the entire request lifecycle.
