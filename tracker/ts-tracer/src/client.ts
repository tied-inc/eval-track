export class EvalTrackClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async putTrace(traceId: string, trace: unknown): Promise<void> {
    const response = await fetch(`${this.baseUrl}/traces/${traceId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(trace),
    });

    if (!response.ok) {
      throw new Error(`Failed to put trace: ${response.statusText}`);
    }
  }

  async getTraces(): Promise<unknown[]> {
    const response = await fetch(`${this.baseUrl}/traces`);
    if (!response.ok) {
      throw new Error(`Failed to get traces: ${response.statusText}`);
    }
    return response.json();
  }
}
