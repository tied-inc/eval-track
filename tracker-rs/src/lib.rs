pub mod client;
pub mod error;
pub mod types;

use once_cell::sync::OnceCell;
use std::cell::RefCell;
use std::sync::Arc;

pub use capture_response_macro::capture_response;
pub use client::TracerClient;
pub use error::TracerError;
pub use types::Trace;

static TRACER_CLIENT: OnceCell<Arc<TracerClient>> = OnceCell::new();
thread_local! {
    static CURRENT_TRACE: RefCell<Option<Trace>> = RefCell::new(None);
}

/// Initialize the global tracer client
pub fn init_tracer(base_url: impl Into<String>) {
    let _ = TRACER_CLIENT.set(Arc::new(TracerClient::new(base_url)));
}

/// Get the global tracer client
pub fn get_tracer() -> Option<Arc<TracerClient>> {
    TRACER_CLIENT.get().cloned()
}

/// Set the current trace for the current thread
pub(crate) fn set_current_trace(trace: Trace) {
    CURRENT_TRACE.with(|current| {
        *current.borrow_mut() = Some(trace);
    });
}

/// Get and clear the current trace for the current thread
pub(crate) fn take_current_trace() -> Option<Trace> {
    CURRENT_TRACE.with(|current| {
        current.borrow_mut().take()
    })
}
