package client

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/tied-inc/eval-track/tracker-go/pkg/trace"
)

func TestNewTracerClient(t *testing.T) {
	tests := []struct {
		name     string
		baseURL  string
		expected string
	}{
		{
			name:     "with custom base URL",
			baseURL:  "http://custom.example.com",
			expected: "http://custom.example.com",
		},
		{
			name:     "with empty base URL",
			baseURL:  "",
			expected: "http://localhost:8000",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			client := NewTracerClient(tt.baseURL)
			assert.Equal(t, tt.expected, client.baseURL)
			assert.NotNil(t, client.httpClient)
		})
	}
}

func TestSendTrace(t *testing.T) {
	tests := []struct {
		name           string
		serverResponse int
		expectError    bool
	}{
		{
			name:           "successful trace send",
			serverResponse: http.StatusOK,
			expectError:    false,
		},
		{
			name:           "server error",
			serverResponse: http.StatusInternalServerError,
			expectError:    true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create test server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// Verify request
				assert.Equal(t, "POST", r.Method)
				assert.Equal(t, "/traces", r.URL.Path)
				assert.Equal(t, "application/json", r.Header.Get("Content-Type"))

				// Verify trace data
				var receivedTrace trace.Trace
				err := json.NewDecoder(r.Body).Decode(&receivedTrace)
				assert.NoError(t, err)
				assert.NotEmpty(t, receivedTrace.ID)

				w.WriteHeader(tt.serverResponse)
			}))
			defer server.Close()

			// Create client with test server URL
			client := NewTracerClient(server.URL)

			// Create test trace
			tr := &trace.Trace{
				FunctionName: "test_function",
				Args:         []interface{}{"arg1", 42},
				Response:     "test response",
			}

			// Send trace
			err := client.SendTrace(context.Background(), tr)

			if tt.expectError {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}
