import { ulid } from "ulid";
import { createTracerClient } from "./client";
import type { Trace } from "./types";

const client = createTracerClient();

export function captureResponse() {
  return (
    target: object,
    propertyKey: string,
    descriptor: PropertyDescriptor,
  ): PropertyDescriptor => {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: unknown[]) {
      const trace: Trace = {
        id: ulid(),
        timestamp: Date.now(),
        function_name: propertyKey,
        args: args,
        kwargs: {},
        response: null,
        error: null,
      };

      try {
        const result = await originalMethod.apply(this, args);
        trace.response = result;
        await client.sendTrace(trace);
        return result;
      } catch (error) {
        trace.error = error;
        await client.sendTrace(trace);
        throw error;
      }
    };

    return descriptor;
  };
}
