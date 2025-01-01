import { z } from "zod";

export const TraceSchema = z.object({
  id: z.string(),
  request: z.object({
    args: z.unknown(),
  }),
  response: z.object({
    result: z.unknown().optional(),
    error: z.string().optional(),
  }),
  created_at: z.string(),
  updated_at: z.string(),
});

export type TraceData = {
  request: {
    args: unknown;
  };
  response: {
    result?: unknown;
    error?: string;
  };
};

export type TracerFunction<T extends (...args: unknown[]) => unknown> = (
  ...args: Parameters<T>
) => Promise<ReturnType<T>>;
