package client

import (
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

// Test functions to be wrapped
func simpleFunction(x int) int {
	return x * 2
}

func errorFunction(x int) (int, error) {
	if x < 0 {
		return 0, errors.New("negative input")
	}
	return x * 2, nil
}

func TestCaptureResponse(t *testing.T) {
	// Create test server
	var receivedTraces int
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		receivedTraces++
		w.WriteHeader(http.StatusOK)
	}))
	defer server.Close()

	// Create client
	client := NewTracerClient(server.URL)

	t.Run("simple function", func(t *testing.T) {
		wrapped := CaptureResponse(simpleFunction, client)
		fn, ok := wrapped.(func(int) int)
		assert.True(t, ok, "wrong function signature")

		result := fn(21)
		assert.Equal(t, 42, result)

		// Wait for async trace to be sent
		time.Sleep(100 * time.Millisecond)
		assert.Equal(t, 1, receivedTraces)
	})

	t.Run("error function success", func(t *testing.T) {
		wrapped := CaptureResponse(errorFunction, client)
		fn, ok := wrapped.(func(int) (int, error))
		assert.True(t, ok, "wrong function signature")

		result, err := fn(21)
		assert.NoError(t, err)
		assert.Equal(t, 42, result)

		// Wait for async trace to be sent
		time.Sleep(100 * time.Millisecond)
		assert.Equal(t, 2, receivedTraces)
	})

	t.Run("error function failure", func(t *testing.T) {
		wrapped := CaptureResponse(errorFunction, client)
		fn, ok := wrapped.(func(int) (int, error))
		assert.True(t, ok, "wrong function signature")

		result, err := fn(-1)
		assert.Error(t, err)
		assert.Equal(t, 0, result)
		assert.Equal(t, "negative input", err.Error())

		// Wait for async trace to be sent
		time.Sleep(100 * time.Millisecond)
		assert.Equal(t, 3, receivedTraces)
	})

	t.Run("non-function panic", func(t *testing.T) {
		assert.Panics(t, func() {
			CaptureResponse("not a function", client)
		})
	})
}
