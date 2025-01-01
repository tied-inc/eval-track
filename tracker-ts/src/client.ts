import type { Trace } from "./types";

export function createTracerClient(
  baseUrl: string = process.env.TRACER_BASE_URL || "http://localhost:8000",
) {
  const sendTrace = async (trace: Trace): Promise<void> => {
    const response = await fetch(`${baseUrl}/traces`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(trace),
    });

    if (!response.ok) {
      throw new Error(`Failed to send trace: ${response.statusText}`);
    }
  };

  return {
    sendTrace,
  };
}
