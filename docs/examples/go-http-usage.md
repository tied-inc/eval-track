# Advanced Go Usage with HTTP Server

This example demonstrates how to use the Go tracer with a standard HTTP server and the Gorilla Mux router, showing function response capture across multiple endpoints and middleware.

## Installation

```bash
go get -u github.com/tied-inc/eval-track/tracker-go
go get -u github.com/gorilla/mux
```

## Basic HTTP Server Integration

```go
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "time"
    
    "github.com/gorilla/mux"
    "github.com/tied-inc/eval-track/tracker-go/pkg/client"
)

// Response types
type ServiceResponse struct {
    Message   string    `json:"message"`
    Timestamp time.Time `json:"timestamp"`
}

type OrchestrationResponse struct {
    Service1     ServiceResponse `json:"service1"`
    Service2     ServiceResponse `json:"service2"`
    OrchestatedAt time.Time      `json:"orchestratedAt"`
}

// Create tracer client
var tracer = client.NewTracerClient("http://localhost:8000")

// Middleware for tracing handlers
func tracedHandler(handler func(http.ResponseWriter, *http.Request) (interface{}, error)) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        wrapped := tracer.CaptureResponse(func() (interface{}, error) {
            return handler(w, r)
        })

        result, err := wrapped()
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(result)
    }
}

// Service handlers
func service1Handler(w http.ResponseWriter, r *http.Request) (interface{}, error) {
    return ServiceResponse{
        Message:   "Service 1 response",
        Timestamp: time.Now(),
    }, nil
}

func service2Handler(w http.ResponseWriter, r *http.Request) (interface{}, error) {
    return ServiceResponse{
        Message:   "Service 2 response",
        Timestamp: time.Now(),
    }, nil
}

// Orchestration handler
func orchestrateHandler(w http.ResponseWriter, r *http.Request) (interface{}, error) {
    // Make internal requests to services
    service1Chan := make(chan ServiceResponse)
    service2Chan := make(chan ServiceResponse)
    errChan := make(chan error)

    go func() {
        resp, err := http.Get("http://localhost:8080/service1")
        if err != nil {
            errChan <- err
            return
        }
        defer resp.Body.Close()

        var result ServiceResponse
        if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
            errChan <- err
            return
        }
        service1Chan <- result
    }()

    go func() {
        resp, err := http.Get("http://localhost:8080/service2")
        if err != nil {
            errChan <- err
            return
        }
        defer resp.Body.Close()

        var result ServiceResponse
        if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
            errChan <- err
            return
        }
        service2Chan <- result
    }()

    var service1Result, service2Result ServiceResponse
    for i := 0; i < 2; i++ {
        select {
        case err := <-errChan:
            return nil, err
        case service1Result = <-service1Chan:
        case service2Result = <-service2Chan:
        }
    }

    return OrchestrationResponse{
        Service1:      service1Result,
        Service2:      service2Result,
        OrchestatedAt: time.Now(),
    }, nil
}

func main() {
    r := mux.NewRouter()

    // Register routes with traced handlers
    r.HandleFunc("/service1", tracedHandler(service1Handler)).Methods("GET")
    r.HandleFunc("/service2", tracedHandler(service2Handler)).Methods("GET")
    r.HandleFunc("/orchestrate", tracedHandler(orchestrateHandler)).Methods("GET")

    // Start server
    log.Fatal(http.ListenAndServe(":8080", r))
}
```

## Advanced Error Handling

```go
// Custom error type
type ServiceError struct {
    Message    string                 `json:"message"`
    StatusCode int                    `json:"statusCode"`
    Context    map[string]interface{} `json:"context,omitempty"`
}

func (e *ServiceError) Error() string {
    return e.Message
}

// Enhanced middleware with error handling
func tracedErrorHandler(handler func(http.ResponseWriter, *http.Request) (interface{}, error)) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        wrapped := tracer.CaptureResponse(func() (interface{}, error) {
            return handler(w, r)
        })

        result, err := wrapped()
        if err != nil {
            var svcErr *ServiceError
            if errors.As(err, &svcErr) {
                w.WriteHeader(svcErr.StatusCode)
                json.NewEncoder(w).Encode(svcErr)
            } else {
                http.Error(w, err.Error(), http.StatusInternalServerError)
            }
            return
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(result)
    }
}

// Usage with custom error handling
func riskyServiceHandler(w http.ResponseWriter, r *http.Request) (interface{}, error) {
    if rand.Float64() > 0.5 {
        return nil, &ServiceError{
            Message:    "Service temporarily unavailable",
            StatusCode: http.StatusServiceUnavailable,
            Context: map[string]interface{}{
                "retryAfter": 30,
            },
        }
    }

    return ServiceResponse{
        Message:   "Service successful",
        Timestamp: time.Now(),
    }, nil
}
```

## Request Context Tracking

```go
// Request context type
type RequestContext struct {
    RequestID string     `json:"requestId"`
    UserID    string     `json:"userId,omitempty"`
    StartTime time.Time  `json:"startTime"`
}

// Context middleware
func contextMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ctx := r.Context()
        requestCtx := &RequestContext{
            RequestID: uuid.New().String(),
            UserID:    r.Header.Get("X-User-ID"),
            StartTime: time.Now(),
        }
        ctx = context.WithValue(ctx, "requestContext", requestCtx)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// Enhanced tracer middleware with context
func tracedContextHandler(handler func(http.ResponseWriter, *http.Request) (interface{}, error)) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        ctx := r.Context()
        requestCtx := ctx.Value("requestContext").(*RequestContext)

        wrapped := tracer.CaptureResponse(func() (interface{}, error) {
            result, err := handler(w, r)
            if err != nil {
                return nil, err
            }

            // Add context to response
            return map[string]interface{}{
                "data":     result,
                "context":  requestCtx,
                "duration": time.Since(requestCtx.StartTime).Milliseconds(),
            }, nil
        })

        result, err := wrapped()
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(result)
    }
}

// Usage with context
func main() {
    r := mux.NewRouter()
    r.Use(contextMiddleware)

    r.HandleFunc("/contextual-service", tracedContextHandler(func(w http.ResponseWriter, r *http.Request) (interface{}, error) {
        ctx := r.Context()
        requestCtx := ctx.Value("requestContext").(*RequestContext)

        return ServiceResponse{
            Message:   fmt.Sprintf("Request %s processed", requestCtx.RequestID),
            Timestamp: time.Now(),
        }, nil
    })).Methods("GET")

    log.Fatal(http.ListenAndServe(":8080", r))
}
```

This example demonstrates:
1. Basic HTTP server integration with traced endpoints
2. Request orchestration using goroutines and channels
3. Advanced error handling with custom error types
4. Request context tracking and duration measurement
5. Middleware composition for tracing and context
6. Type safety with struct definitions

The tracer captures all responses and errors automatically, providing observability across the entire request lifecycle.
