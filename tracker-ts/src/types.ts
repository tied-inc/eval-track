import type { z } from "zod";
import { z as zod } from "zod";

/**
 * TraceSchema represents the TypeScript equivalent of Python's Trace model,
 * combining fields from both entity.py and tracer.py implementations.
 *
 * Fields from Python's entity.py:
 * - id: Unique identifier for the trace (uses ULID like Python)
 * - response: Captured function response (equivalent to Python's response field)
 *
 * Additional fields from tracer.py's capture_response decorator:
 * - timestamp: Capture time (replaces Python's created_at/updated_at)
 * - function_name: Name of the decorated function being traced
 * - args: Positional arguments passed to the function
 * - kwargs: Keyword arguments passed to the function
 * - error: Any error that occurred during function execution
 */
export const TraceSchema = zod.object({
  id: zod.string(),
  timestamp: zod.number(),
  function_name: zod.string(),
  args: zod.array(zod.unknown()),
  kwargs: zod.record(zod.unknown()),
  response: zod.unknown(),
  error: zod.unknown().nullable(),
});

export type Trace = z.infer<typeof TraceSchema>;
