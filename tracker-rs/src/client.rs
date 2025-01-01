use crate::error::TracerError;
use crate::types::Trace;
use reqwest::Client;
use std::sync::Arc;

#[derive(Clone)]
pub struct TracerClient {
    base_url: String,
    http_client: Arc<Client>,
}

impl TracerClient {
    pub fn new(base_url: impl Into<String>) -> Self {
        Self {
            base_url: base_url.into(),
            http_client: Arc::new(Client::new()),
        }
    }

    pub async fn put_trace(&self, trace: &Trace) -> Result<(), TracerError> {
        let url = format!("{}/traces", self.base_url);
        self.http_client
            .post(&url)
            .json(trace)
            .send()
            .await?
            .error_for_status()?;
        Ok(())
    }

    pub async fn get_traces(&self) -> Result<Vec<Trace>, TracerError> {
        let url = format!("{}/traces", self.base_url);
        let resp = self.http_client
            .get(&url)
            .send()
            .await?
            .error_for_status()?;
        Ok(resp.json().await?)
    }
}
