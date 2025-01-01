import { Trace } from "./types";

export class TracerClient {
  private baseUrl: string;

  constructor(baseUrl: string = process.env.TRACER_BASE_URL || "http://localhost:8000") {
    this.baseUrl = baseUrl;
  }

  async sendTrace(trace: Trace): Promise<void> {
    const response = await fetch(`${this.baseUrl}/traces`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(trace),
    });

    if (!response.ok) {
      throw new Error(`Failed to send trace: ${response.statusText}`);
    }
  }
}
