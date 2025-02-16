// src/tests//utils/append-with-space.test.ts

import { describe, test, expect } from "@jest/globals";
import { concatenateChunkWithSpace } from "../../utils/stream";

describe("concatenateChunkWithSpace", () => {
  test("should return chunk if buffer is empty", () => {
    const result = concatenateChunkWithSpace("", "world");
    expect(result).toBe("world");
  });

  test("should append a space between buffer and chunk when needed", () => {
    const result = concatenateChunkWithSpace("Hello", "world");
    expect(result).toBe("Hello world");
  });

  test("should not add extra space if buffer ends with a space", () => {
    const result = concatenateChunkWithSpace("Hello ", "world");
    expect(result).toBe("Hello world");
  });

  test("should not add extra space if chunk starts with a space", () => {
    const result = concatenateChunkWithSpace("Hello", " world");
    expect(result).toBe("Hello world");
  });

  test("should return concatenation when both buffer and chunk have spaces", () => {
    const result = concatenateChunkWithSpace("Hello ", " world");
    // In this case, it simply concatenates the two strings.
    expect(result).toBe("Hello  world");
  });

  test("should handle both empty buffer and empty chunk", () => {
    const result = concatenateChunkWithSpace("", "");
    expect(result).toBe("");
  });

  test("should handle non-empty buffer and empty chunk", () => {
    const result = concatenateChunkWithSpace("Hello", "");
    expect(result).toBe("Hello");
  });
});
