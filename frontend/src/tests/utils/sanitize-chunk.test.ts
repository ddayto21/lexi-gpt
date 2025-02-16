// src/tests/utils/clean-chunk.test.ts

import { describe, test, expect } from "@jest/globals";
import { sanitizeChunk } from "../../utils/stream";

describe("sanitizeChunk", () => {
  test("should trim whitespace", () => {
    expect(sanitizeChunk("   hello   ")).toBe("hello");
  });

  test("should remove leading '```json' marker", () => {
    expect(sanitizeChunk("```json hello world")).toBe("hello world");
  });

  test("should remove trailing '```' marker", () => {
    expect(sanitizeChunk("hello world ```")).toBe("hello world");
  });

  test("should remove both leading and trailing markers with extra whitespace", () => {
    expect(sanitizeChunk("   ```json   hello world   ```   ")).toBe("hello world");
  });
});
