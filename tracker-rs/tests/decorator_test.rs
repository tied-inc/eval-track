use eval_track_rust::{init_tracer, capture_response};
use wiremock::{MockServer, Mock, ResponseTemplate};
use wiremock::matchers::{method, path};
use tokio;

#[tokio::test]
async fn test_async_capture_response() {
    // Start mock server
    let mock_server = MockServer::start().await;

    // Create a mock response
    Mock::given(method("PUT"))
        .and(path("/traces"))
        .respond_with(ResponseTemplate::new(200))
        .mount(&mock_server)
        .await;

    // Initialize tracer with mock server
    init_tracer(mock_server.uri());

    // Define test function with capture_response
    #[capture_response]
    async fn test_function(x: i32) -> Result<i32, String> {
        Ok(x * 2)
    }

    // Test the function
    let result = test_function(5).await;
    assert!(result.is_ok());
    assert_eq!(result.unwrap(), 10);
}

#[test]
fn test_sync_capture_response() {
    // Start runtime for sync test
    let rt = tokio::runtime::Runtime::new().unwrap();
    
    // Start mock server in runtime
    let mock_server = rt.block_on(async {
        let server = MockServer::start().await;
        Mock::given(method("PUT"))
            .and(path("/traces"))
            .respond_with(ResponseTemplate::new(200))
            .mount(&server)
            .await;
        server
    });

    // Initialize tracer with mock server
    init_tracer(mock_server.uri());

    // Define test function with capture_response
    #[capture_response]
    fn test_function(x: i32) -> Result<i32, String> {
        Ok(x * 2)
    }

    // Test the function
    let result = test_function(5);
    assert!(result.is_ok());
    assert_eq!(result.unwrap(), 10);
}

#[tokio::test]
async fn test_capture_response_error() {
    let mock_server = MockServer::start().await;

    Mock::given(method("PUT"))
        .and(path("/traces"))
        .respond_with(ResponseTemplate::new(200))
        .mount(&mock_server)
        .await;

    init_tracer(mock_server.uri());

    #[capture_response]
    async fn test_function() -> Result<(), String> {
        Err("test error".to_string())
    }

    let result = test_function().await;
    assert!(result.is_err());
    assert_eq!(result.unwrap_err(), "test error");
}
