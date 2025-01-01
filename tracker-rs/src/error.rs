use thiserror::Error;

#[derive(Debug, Error)]
pub enum TracerError {
    #[error("HTTP error occurred: {0}")]
    Http(#[from] reqwest::Error),

    #[error("Serialization error occurred: {0}")]
    Serialization(#[from] serde_json::Error),

    #[error("Unknown error: {0}")]
    Unknown(String),
}
