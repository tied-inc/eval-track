import { ulid } from "ulid";
import { EvalTrackClient } from "./client";
import { type TraceData, TraceSchema, type TracerFunction } from "./types";


export function captureResponse<T extends (...args: unknown[]) => unknown>(
  fn: T,
): TracerFunction<T> {
  return async (...args: Parameters<T>): Promise<ReturnType<T>> => {
    const traceId = ulid();
    const startTime = new Date().toISOString();

    try {
      const result = await Promise.resolve(fn(...args));

      // Validate and store the trace data
      const traceData: TraceData = {
        request: { args },
        response: { result },
      };

      const trace = TraceSchema.parse({
        id: traceId,
        ...traceData,
        created_at: startTime,
        updated_at: new Date().toISOString(),
      });

      // Create client and store trace asynchronously without waiting
      const client = new EvalTrackClient(
        process.env.EVAL_TRACKER_HOST ?? "http://localhost:8000",
      );
      client.putTrace(traceId, trace).catch((error) => {
        console.error("Failed to store trace:", error);
      });

      return result as ReturnType<T>;
    } catch (error) {
      // Still try to store the trace even if the function fails
      const traceData: TraceData = {
        request: { args },
        response: { error: String(error) },
      };

      const trace = TraceSchema.parse({
        id: traceId,
        ...traceData,
        created_at: startTime,
        updated_at: new Date().toISOString(),
      });

      const client = new EvalTrackClient(
        process.env.EVAL_TRACKER_HOST ?? "http://localhost:8000",
      );
      client.putTrace(traceId, trace).catch((storeError) => {
        console.error("Failed to store error trace:", storeError);
      });

      throw error;
    }
  };
}

export { EvalTrackClient };
