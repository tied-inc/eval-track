# Go Tracer

A Go implementation of the eval-track tracer for capturing function responses in Go applications.

## Installation

### Prerequisites
- Go version 1.20 or higher
- Working Go environment (GOPATH configured)
- [Task](https://taskfile.dev/) (optional, for development tasks)

### Install using go get
```bash
go get github.com/tied-inc/eval-track/tracker-go
```

### Install using Task (recommended for development)
```bash
# Install Task if not already installed
npm install -g @go-task/cli

# Install dependencies
task install-tracker
```

## Environment Setup

### Configuration

The tracer can be configured through the following environment variables:

| Variable Name      | Purpose                                          | Default Value            |
|-------------------|--------------------------------------------------|-------------------------|
| EVAL_TRACK_API_URL| Base URL for the eval-track API                  | http://localhost:8000   |
| DEBUG             | Enable debug logging (set to true/false)         | false                   |
| GO_ENV            | Environment mode (development/production)         | development             |
| TRACE_TIMEOUT     | Timeout for trace operations (in seconds)        | 30                      |

## Basic Usage

```go
package main

import (
    "fmt"
    "github.com/tied-inc/eval-track/tracker-go/pkg/client"
)

func main() {
    // Create a new tracer client
    tracer := client.NewTracerClient("http://localhost:8000")

    // Basic function with return value
    wrappedFn := tracer.CaptureResponse(func() (string, error) {
        return "Hello, World!", nil
    })

    // Use the wrapped function
    result, err := wrappedFn()
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    fmt.Println(result)

    // Function with parameters
    greet := tracer.CaptureResponse(func(name string) (string, error) {
        return fmt.Sprintf("Hello, %s!", name), nil
    })

    // Call the wrapped function
    greeting, err := greet("Alice")
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    fmt.Println(greeting)
}
```

## Error Handling

The tracer automatically captures both successful responses and errors:

```go
package main

import (
    "errors"
    "fmt"
    "github.com/tied-inc/eval-track/tracker-go/pkg/client"
)

func main() {
    tracer := client.NewTracerClient("http://localhost:8000")

    // Function that might return an error
    riskyOperation := tracer.CaptureResponse(func(input int) (string, error) {
        if input < 0 {
            return "", errors.New("input must be non-negative")
        }
        return fmt.Sprintf("Processed %d", input), nil
    })

    // Success case
    result, err := riskyOperation(42)
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    fmt.Println(result)

    // Error case
    result, err = riskyOperation(-1)
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
}
```

## Advanced Usage

### Struct Methods

```go
package main

import (
    "github.com/tied-inc/eval-track/tracker-go/pkg/client"
)

type Service struct {
    tracer *client.TracerClient
}

func NewService(tracerURL string) *Service {
    return &Service{
        tracer: client.NewTracerClient(tracerURL),
    }
}

func (s *Service) ProcessData(data []byte) ([]byte, error) {
    processFunc := s.tracer.CaptureResponse(func(input []byte) ([]byte, error) {
        // Process the data
        return input, nil
    })

    return processFunc(data)
}
```

### HTTP Handler Integration

```go
package main

import (
    "encoding/json"
    "net/http"
    "github.com/tied-inc/eval-track/tracker-go/pkg/client"
)

type Response struct {
    Message string `json:"message"`
}

func main() {
    tracer := client.NewTracerClient("http://localhost:8000")

    // Wrap an HTTP handler
    handler := func(w http.ResponseWriter, r *http.Request) {
        wrappedLogic := tracer.CaptureResponse(func() (*Response, error) {
            return &Response{Message: "Hello from HTTP handler"}, nil
        })

        result, err := wrappedLogic()
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        json.NewEncoder(w).Encode(result)
    }

    http.HandleFunc("/", handler)
    http.ListenAndServe(":8080", nil)
}
```

## Troubleshooting

### Common Issues

1. **Function Signature Errors**
   - Ensure wrapped functions return (T, error)
   - Check that function parameters match expected types
   - Verify struct method receivers are correctly defined

2. **Network Issues**
   - Check EVAL_TRACK_API_URL configuration
   - Verify network connectivity
   - Check for firewall or proxy settings

3. **Reflection Errors**
   - Ensure function types are compatible with reflection
   - Check for unexported struct fields
   - Verify interface implementations

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
DEBUG=eval-track:*
```

## Features


- Generates unique trace IDs using ULID
- Supports both successful responses and errors
- Uses reflection to preserve function signatures
- Thread-safe client implementation
- Automatic JSON serialization of responses
- Support for struct methods and closures
- Compatible with standard library HTTP handlers

## Further Reading

For more detailed information about the tracer implementation and API reference, see the [official documentation](/docs/tracer.md).

## Contributing

Please refer to the project's contributing guidelines for information about making contributions to this package.
