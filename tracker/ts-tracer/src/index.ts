import { ulid } from "ulid";
import { TracerClient } from "./client";
import { Trace } from "./types";

const client = new TracerClient();

export function captureResponse() {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
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
