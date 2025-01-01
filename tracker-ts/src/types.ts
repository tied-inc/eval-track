import { z } from "zod";

export const TraceSchema = z.object({
  id: z.string(),
  timestamp: z.number(),
  function_name: z.string(),
  args: z.array(z.unknown()),
  kwargs: z.record(z.unknown()),
  response: z.unknown(),
  error: z.unknown().nullable(),
});

export type Trace = z.infer<typeof TraceSchema>;
