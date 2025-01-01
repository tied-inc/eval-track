use eval_track_rust::{TracerClient, Trace};
use wiremock::{MockServer, Mock, ResponseTemplate};
use wiremock::matchers::{method, path};
use serde_json::json;
use tokio;

#[tokio::test]
async fn test_put_trace_success() {
    // Start mock server
    let mock_server = MockServer::start().await;

    // Create a mock response
    Mock::given(method("PUT"))
        .and(path("/traces"))
        .respond_with(ResponseTemplate::new(200))
        .mount(&mock_server)
        .await;

    // Create client with mock server URL
    let client = TracerClient::new(mock_server.uri());

    // Create a test trace
    let trace = Trace {
        id: "test-id".to_string(),
        request: json!({"test": "request"}),
        response: json!({"test": "response"}),
        created_at: chrono::Utc::now(),
        updated_at: chrono::Utc::now(),
    };

    // Test put_trace
    let result = client.put_trace(&trace).await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_put_trace_server_error() {
    let mock_server = MockServer::start().await;

    Mock::given(method("PUT"))
        .and(path("/traces"))
        .respond_with(ResponseTemplate::new(500))
        .mount(&mock_server)
        .await;

    let client = TracerClient::new(mock_server.uri());
    let trace = Trace {
        id: "test-id".to_string(),
        request: json!({"test": "request"}),
        response: json!({"test": "response"}),
        created_at: chrono::Utc::now(),
        updated_at: chrono::Utc::now(),
    };

    let result = client.put_trace(&trace).await;
    assert!(result.is_err());
}
