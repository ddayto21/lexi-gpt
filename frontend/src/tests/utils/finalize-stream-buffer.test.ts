// src/tests/utils/finalize-stream-buffer.test.ts

import { describe, test, expect } from "@jest/globals";
import { finalizeStreamBuffer } from "../../utils/stream";

describe("finalizeStreamBuffer", () => {
  test("returns done true with empty buffer when input is exactly '[DONE]'", () => {
    const result = finalizeStreamBuffer("[DONE]");
    expect(result).toEqual({ buffer: "", done: true });
  });

  test("removes '[DONE]' marker from buffer and marks done true", () => {
    const input = "hello [DONE] world";
    const expected = { buffer: "hello world", done: true };
    expect(finalizeStreamBuffer(input)).toEqual(expected);
  });

  test("returns original buffer and done false when no marker is found", () => {
    const input = "hello world";
    const expected = { buffer: "hello world", done: false };
    expect(finalizeStreamBuffer(input)).toEqual(expected);
  });

  test("removes '[DONE]' marker and trims extra whitespace", () => {
    const input = "   hello [DONE]   ";
    const expected = { buffer: "hello", done: true };
    expect(finalizeStreamBuffer(input)).toEqual(expected);
  });

  test("handles multiple occurrences of '[DONE]' by only removing the first occurrence", () => {
    const input = "[DONE] hello [DONE] world [DONE]";
    // Note: String.replace() only removes the first occurrence, so the expected output retains later markers.
    const expected = { buffer: "hello [DONE] world [DONE]", done: true };
    expect(finalizeStreamBuffer(input)).toEqual(expected);
  });
});
