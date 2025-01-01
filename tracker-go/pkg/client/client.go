package client

import (
	"bytes"
	"context"
	"crypto/rand"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"time"

	"github.com/oklog/ulid"
	"github.com/tied-inc/eval-track/tracker-go/pkg/trace"
)

// TracerClient handles sending trace data to the server.
// It maintains a baseURL for the API endpoint and an HTTP client for making requests.
type TracerClient struct {
	baseURL    string
	httpClient *http.Client
}

// NewTracerClient creates a new TracerClient instance.
// If no baseURL is provided, it defaults to "http://localhost:8000".
func NewTracerClient(baseURL string) *TracerClient {
	if baseURL == "" {
		baseURL = "http://localhost:8000"
	}
	return &TracerClient{
		baseURL:    baseURL,
		httpClient: &http.Client{},
	}
}

// SendTrace sends the trace data to the server.
// If the trace ID is empty, it generates a new ULID.
// The trace is sent as a POST request to baseURL/traces.
func (tc *TracerClient) SendTrace(ctx context.Context, tr *trace.Trace) error {
	if tr.ID == "" {
		tr.ID = ulid.MustNew(ulid.Timestamp(time.Now()), rand.Reader).String()
	}

	data, err := json.Marshal(tr)
	if err != nil {
		return fmt.Errorf("failed to marshal trace: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, "POST", tc.baseURL+"/traces", bytes.NewBuffer(data))
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := tc.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("failed to send request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return errors.New("server returned non-200 status code: " + resp.Status)
	}

	return nil
}
