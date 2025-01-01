#[cfg(feature = "integration-tests")]
mod tests {
    use serde_json::json;
    use std::time::Duration;
    use tokio;
    use tracker::{capture_response, init_tracer, TracerClient};
    use wiremock::matchers::{body_json_schema, method, path};
    use wiremock::{Mock, MockServer, ResponseTemplate};

    #[tokio::test]
    async fn test_full_trace_lifecycle() {
        // Start mock server
        let mock_server = MockServer::start().await;

        // Create a mock response with schema validation
        Mock::given(method("PUT"))
            .and(path("/traces"))
            .and(body_json_schema(json!({
                "type": "object",
                "required": ["id", "request", "response", "created_at", "updated_at"],
                "properties": {
                    "id": { "type": "string" },
                    "request": { "type": "object" },
                    "response": { "type": "object" },
                    "created_at": { "type": "string" },
                    "updated_at": { "type": "string" }
                }
            })))
            .respond_with(ResponseTemplate::new(200))
            .mount(&mock_server)
            .await;

        // Initialize tracer
        init_tracer(mock_server.uri());

        // Define test functions
        #[capture_response]
        async fn async_test_function(x: i32, y: String) -> Result<String, String> {
            tokio::time::sleep(Duration::from_millis(100)).await;
            Ok(format!("{} - {}", x, y))
        }

        #[capture_response]
        fn sync_test_function(x: i32) -> Result<i32, String> {
            Ok(x * 2)
        }

        // Test async function
        let async_result = async_test_function(42, "test".to_string()).await;
        assert!(async_result.is_ok());
        assert_eq!(async_result.unwrap(), "42 - test");

        // Test sync function
        let sync_result = sync_test_function(21);
        assert!(sync_result.is_ok());
        assert_eq!(sync_result.unwrap(), 42);

        // Allow time for traces to be sent
        tokio::time::sleep(Duration::from_millis(200)).await;
    }

    #[tokio::test]
    async fn test_error_trace_capture() {
        let mock_server = MockServer::start().await;

        Mock::given(method("PUT"))
            .and(path("/traces"))
            .and(body_json_schema(json!({
                "type": "object",
                "required": ["id", "request", "response", "created_at", "updated_at"],
                "properties": {
                    "id": { "type": "string" },
                    "request": { "type": "object" },
                    "response": {
                        "type": "object",
                        "required": ["error"],
                        "properties": {
                            "error": { "type": "string" }
                        }
                    },
                    "created_at": { "type": "string" },
                    "updated_at": { "type": "string" }
                }
            })))
            .respond_with(ResponseTemplate::new(200))
            .mount(&mock_server)
            .await;

        init_tracer(mock_server.uri());

        #[capture_response]
        async fn failing_function() -> Result<(), String> {
            Err("intentional error".to_string())
        }

        let result = failing_function().await;
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "intentional error");

        tokio::time::sleep(Duration::from_millis(200)).await;
    }

    #[tokio::test]
    async fn test_trace_data_compatibility() {
        let mock_server = MockServer::start().await;
        let received_traces = std::sync::Arc::new(tokio::sync::Mutex::new(Vec::new()));
        let traces_clone = received_traces.clone();

        Mock::given(method("PUT"))
            .and(path("/traces"))
            .respond_with(ResponseTemplate::new(200).set_body_json(json!({"status": "ok"})))
            .and(move |req| {
                let traces = traces_clone.clone();
                let body: serde_json::Value = serde_json::from_slice(&req.body).unwrap();
                tokio::spawn(async move {
                    traces.lock().await.push(body);
                });
                true
            })
            .mount(&mock_server)
            .await;

        init_tracer(mock_server.uri());

        #[capture_response]
        async fn test_function(input: String) -> Result<String, String> {
            Ok(input.to_uppercase())
        }

        let result = test_function("hello".to_string()).await;
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "HELLO");

        tokio::time::sleep(Duration::from_millis(200)).await;

        let traces = received_traces.lock().await;
        assert_eq!(traces.len(), 1);

        let trace = &traces[0];
        assert!(trace["id"].is_string());
        assert!(trace["request"].is_object());
        assert!(trace["response"].is_object());
        assert!(trace["created_at"].is_string());
        assert!(trace["updated_at"].is_string());

        // Verify request format matches other implementations
        let request = &trace["request"];
        assert!(request["args"].is_string());

        // Verify response format matches other implementations
        let response = &trace["response"];
        assert!(response["data"].is_string() || response["error"].is_string());
    }
}
