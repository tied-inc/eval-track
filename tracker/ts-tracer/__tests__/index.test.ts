import { ulid } from "ulid";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { EvalTrackClient } from "../src/client";
import { captureResponse } from "../src/index";
import { TraceSchema } from "../src/types";

// Mock the EvalTrackClient
const mockPutTrace = vi.fn().mockResolvedValue(undefined);
const mockGetTraces = vi.fn().mockResolvedValue([]);

vi.mock("../src/client", () => ({
  EvalTrackClient: vi.fn().mockImplementation(() => ({
    putTrace: mockPutTrace,
    getTraces: mockGetTraces,
  })),
}));

beforeEach(() => {
  vi.clearAllMocks();
});

describe("captureResponse", () => {
  it("should generate valid ULID for trace ID", async () => {
    const testFunc = async () => ({ data: "test" });
    const wrapped = captureResponse(testFunc);
    await wrapped();

    expect(mockPutTrace).toHaveBeenCalledTimes(1);
    const [traceId] = mockPutTrace.mock.calls[0];
    // ULID is 26 characters long and follows a specific pattern
    expect(traceId).toMatch(/^[0-9A-HJKMNP-TV-Z]{26}$/);
    expect(traceId.length).toBe(26);
  });

  it("should validate response data with zod schema", async () => {
    const testData = {
      id: ulid(),
      request: { args: "test" },
      response: { result: "result" },
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    expect(() => TraceSchema.parse(testData)).not.toThrow();
  });

  it("should capture response from async function", async () => {
    const testFunc = async () => ({ data: "async test" });
    const wrapped = captureResponse(testFunc);
    const result = await wrapped();

    expect(result).toEqual({ data: "async test" });
    expect(mockPutTrace).toHaveBeenCalledTimes(1);
  });

  it("should capture response from sync function", async () => {
    const testFunc = () => ({ data: "sync test" });
    const wrapped = captureResponse(testFunc);
    const result = await wrapped();

    expect(result).toEqual({ data: "sync test" });
    expect(mockPutTrace).toHaveBeenCalledTimes(1);
  });
});
