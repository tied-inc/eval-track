use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, ItemFn};

#[proc_macro_attribute]
pub fn capture_response(_attr: TokenStream, item: TokenStream) -> TokenStream {
    let input_fn = parse_macro_input!(item as ItemFn);
    let fn_name = &input_fn.sig.ident;
    let fn_inputs = &input_fn.sig.inputs;
    let fn_output = &input_fn.sig.output;
    let fn_block = &input_fn.block;
    let fn_vis = &input_fn.vis;
    let fn_asyncness = &input_fn.sig.asyncness;

    let expanded = if fn_asyncness.is_some() {
        quote! {
            #fn_vis #fn_asyncness fn #fn_name #fn_inputs #fn_output {
                use ulid::Ulid;
                use chrono::Utc;
                use serde_json::json;

                let trace_id = Ulid::new().to_string();
                let now = Utc::now();
                let request = json!({
                    "args": format!("{:?}", (#fn_inputs))
                });

                let result = #fn_block;
                let response = match &result {
                    Ok(v) => json!({"data": v}),
                    Err(e) => json!({"error": format!("{:?}", e)})
                };

                let trace = crate::types::Trace {
                    id: trace_id,
                    request,
                    response,
                    created_at: now,
                    updated_at: now,
                };

                if let Some(tracer) = crate::get_tracer() {
                    crate::set_current_trace(trace.clone());
                    let _ = tracer.put_trace(&trace).await;
                }

                result
            }
        }
    } else {
        quote! {
            #fn_vis fn #fn_name #fn_inputs #fn_output {
                use ulid::Ulid;
                use chrono::Utc;
                use serde_json::json;

                let trace_id = Ulid::new().to_string();
                let now = Utc::now();
                let request = json!({
                    "args": format!("{:?}", (#fn_inputs))
                });

                let result = #fn_block;
                let response = match &result {
                    Ok(v) => json!({"data": v}),
                    Err(e) => json!({"error": format!("{:?}", e)})
                };

                let trace = crate::types::Trace {
                    id: trace_id,
                    request,
                    response,
                    created_at: now,
                    updated_at: now,
                };

                if let Some(tracer) = crate::get_tracer() {
                    crate::set_current_trace(trace.clone());
                    let rt = tokio::runtime::Runtime::new().unwrap();
                    let _ = rt.block_on(tracer.put_trace(&trace));
                }

                result
            }
        }
    };

    TokenStream::from(expanded)
}
