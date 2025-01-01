package client

import (
	"context"
	"errors"
	"reflect"
	"runtime"

	"github.com/tied-inc/eval-track/tracker-go/pkg/trace"
)

// ErrNotAFunction is returned when the provided interface{} is not a function
var ErrNotAFunction = errors.New("provided interface is not a function")

// CaptureResponse wraps a function and captures its response for tracing.
// It supports both synchronous and asynchronous functions that return either:
// - A single value
// - A value and an error
// The wrapped function maintains the same signature as the original function.
func CaptureResponse(fn interface{}, tc *TracerClient) interface{} {
	// Get the function name for tracing
	fnValue := reflect.ValueOf(fn)
	if fnValue.Kind() != reflect.Func {
		panic(ErrNotAFunction)
	}

	// Get the actual function name using runtime reflection
	functionName := runtime.FuncForPC(fnValue.Pointer()).Name()

	// Get the function type for creating the wrapper
	fnType := fnValue.Type()

	// Create a wrapper function with the same signature
	wrapper := reflect.MakeFunc(fnType, func(args []reflect.Value) []reflect.Value {
		// Convert args to []interface{} for trace
		traceArgs := make([]interface{}, len(args))
		for i, arg := range args {
			if arg.CanInterface() {
				traceArgs[i] = arg.Interface()
			}
		}

		// Create trace
		tr := trace.NewTrace(functionName, traceArgs)

		// Call original function
		results := fnValue.Call(args)

		// Process results based on return signature
		if len(results) == 2 { // (value, error) case
			result := results[0].Interface()
			tr.Response = result

			if errVal := results[1].Interface(); errVal != nil {
				if err, ok := errVal.(error); ok {
					tr.Error = err.Error()
				}
			}
		} else if len(results) == 1 { // single return value case
			tr.Response = results[0].Interface()
		}

		// Send trace asynchronously to not block the function
		go func() {
			if err := tc.SendTrace(context.Background(), tr); err != nil {
				// We can't return this error as it would change the function signature
				// In a production environment, you might want to use a logger here
				_ = err
			}
		}()

		return results
	})

	return wrapper.Interface()
}
