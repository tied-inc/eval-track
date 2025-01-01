import { describe, expect, it, vi } from "vitest";
import { captureResponse } from "../src";
import { createTracerClient } from "../src/client";

vi.mock("../src/client", () => ({
  createTracerClient: vi.fn().mockImplementation(() => ({
    sendTrace: vi.fn().mockResolvedValue(undefined),
  })),
}));

describe("captureResponse", () => {
  it("should capture successful function execution", async () => {
    class TestClass {
      @captureResponse()
      async testMethod(a: number, b: number): Promise<number> {
        return a + b;
      }
    }

    const instance = new TestClass();
    const result = await instance.testMethod(1, 2);

    expect(result).toBe(3);
    expect(createTracerClient).toHaveBeenCalled();
  });

  it("should capture function errors", async () => {
    class TestClass {
      @captureResponse()
      async testMethod(): Promise<void> {
        throw new Error("Test error");
      }
    }

    const instance = new TestClass();
    await expect(instance.testMethod()).rejects.toThrow("Test error");
    expect(createTracerClient).toHaveBeenCalled();
  });
});
