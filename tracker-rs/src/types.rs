use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Trace {
    pub id: String,      // ULID
    pub request: Value,  // generic JSON payload
    pub response: Value, // generic JSON payload
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}
