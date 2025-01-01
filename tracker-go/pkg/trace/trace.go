package trace

import (
	"crypto/rand"
	"time"

	"github.com/oklog/ulid"
)

// Trace represents the Go equivalent of Python's Trace model and TypeScript's TraceSchema.
// It combines fields from both implementations to maintain compatibility across languages.
type Trace struct {
	// ID is a unique identifier for the trace using ULID
	ID string `json:"id"`

	// Timestamp represents when the trace was created (Unix milliseconds)
	Timestamp int64 `json:"timestamp"`

	// FunctionName is the name of the decorated function being traced
	FunctionName string `json:"function_name"`

	// Args contains the positional arguments passed to the function
	Args []interface{} `json:"args"`

	// Kwargs contains the keyword arguments passed to the function
	Kwargs map[string]interface{} `json:"kwargs"`

	// Response holds the function's return value
	Response interface{} `json:"response"`

	// Error contains any error message if the function execution failed
	Error string `json:"error,omitempty"`
}

// NewTrace creates a new Trace instance with a generated ULID and current timestamp.
// It initializes the trace with the given function name and arguments.
func NewTrace(functionName string, args []interface{}) *Trace {
	return &Trace{
		ID:           ulid.MustNew(ulid.Timestamp(time.Now()), rand.Reader).String(),
		Timestamp:    time.Now().UnixMilli(),
		FunctionName: functionName,
		Args:         args,
		Kwargs:       make(map[string]interface{}),
	}
}
