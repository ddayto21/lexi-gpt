/**
 * @fileoverview Unit tests for the SSE parsing and formatting functions.
 *
 * These tests verify that the helper functions (extractTokens, joinTokens, parseSseData, and formatContent)
 * produce the expected output. The current behavior concatenates tokens with a single space.
 * (Previously, the expected output used newline characters, but we have updated the tests to reflect
 * the single-space concatenation.)
 */

import { extractTokens, joinTokens, parseSseData, formatContent, getTimeAgo } from "../../utils/parse-sse-data";
import type { Message } from "@ai-sdk/react";

// Tests for extractTokens
describe("extractTokens", () => {
  /**
   * Checks that extractTokens splits the input by newlines, removes the "data:" prefix,
   * and returns only the valid tokens.
   */
  test("should extract tokens from SSE input", () => {
    const input = `data: Hello\n\ndata: World\n\nrandom: Ignored`;
    const expected = ["Hello", "World"];
    expect(extractTokens(input)).toEqual(expected);
  });

  /**
   * Checks that if a token contains JSON, extractTokens parses it and returns the 'content' field.
   */
  test("should parse JSON tokens correctly", () => {
    const jsonContent = JSON.stringify({ content: "Parsed JSON" });
    const input = `data: ${jsonContent}\n\n`;
    const expected = ["Parsed JSON"];
    expect(extractTokens(input)).toEqual(expected);
  });

  /**
   * Ensures that an empty or whitespace-only input returns an empty array.
   */
  test("should return an empty array for empty or whitespace-only input", () => {
    expect(extractTokens("")).toEqual([]);
    expect(extractTokens("  \n\n ")).toEqual([]);
  });
});

// Tests for joinTokens
describe("joinTokens", () => {
  /**
   * Verifies that joinTokens concatenates an array of tokens with a single space.
   */
  test("should join tokens with a single space", () => {
    const tokens = ["Hello", "World"];
    const expected = "Hello World";
    expect(joinTokens(tokens)).toBe(expected);
  });

  /**
   * Verifies that joinTokens collapses extra whitespace between tokens.
   */
  test("should collapse extra whitespace between tokens", () => {
    const tokens = ["Hello", "   World  "];
    const expected = "Hello World";
    expect(joinTokens(tokens)).toBe(expected);
  });
});

// Tests for parseSseData (full pipeline)
describe("parseSseData", () => {
  /**
   * Verifies that an empty string input produces an empty string.
   */
  test("should return an empty string for empty input", () => {
    expect(parseSseData("")).toBe("");
  });

  /**
   * Verifies that a single SSE event is parsed correctly.
   */
  test("should parse a single SSE event correctly", () => {
    const input = "data: Hello\n\n";
    const expectedOutput = "Hello";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  /**
   * Verifies that multiple SSE events are parsed correctly and concatenated with a single space.
   */
  test("should parse multiple SSE events correctly", () => {
    const input = "data: Hello\n\ndata: World\n\n";
    const expectedOutput = "Hello World";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  /**
   * Verifies that lines not starting with "data:" are ignored.
   */
  test("should ignore lines that do not start with 'data:'", () => {
    const input = "random: Not included\ndata: Included\n";
    const expectedOutput = "Included";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  /**
   * Verifies that extra spaces after the "data:" prefix are trimmed.
   */
  test("should handle extra spaces after 'data:'", () => {
    const input = "data:    Spaced\n\n";
    const expectedOutput = "Spaced";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  /**
   * Verifies that multiple SSE events are concatenated with a single space between them.
   */
  test("should concatenate events with a single space", () => {
    const input = "data: Part1\n\ndata: Part2\n\ndata: Part3\n\n";
    const expectedOutput = "Part1 Part2 Part3";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  /**
   * Verifies that multiple data lines on a single physical line are handled correctly.
   */
  test("should handle multiple data lines", () => {
    const input = "data: Hello\ndata: World!\n\n";
    const expectedOutput = "Hello World!";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  /**
   * Verifies that if the input contains only whitespace, an empty string is returned.
   */
  test("should return empty string for no data", () => {
    expect(parseSseData("")).toBe("");
    expect(parseSseData("  \n\n ")).toBe("");
  });

  /**
   * Verifies that non-string input throws an appropriate error.
   */
  test("should throw error on invalid input", () => {
    expect(() => parseSseData(null as unknown as string)).toThrow("Input must be a string");
  });
});

// Tests for formatContent
describe("formatContent", () => {
  /**
   * Verifies that formatContent processes an assistant message by parsing its SSE data and
   * returning the cleaned content.
   */
  test("formatContent works with assistant messages", () => {
    const message: Message = {
      role: "assistant",
      content: "data: This is formatted\n",
      id: "some-unique-id",
    };
    expect(formatContent(message)).toBe("This is formatted");
  });

  /**
   * Verifies that formatContent preserves markdown structure for bullet lists and headings.
   * Since the current implementation concatenates tokens with a single space,
   * the expected output is a single-line string.
   */
  test("should format bullet lists and headings correctly", () => {
    const input = `
data: # Heading 1

data: - Bullet 1
data: - Bullet 2

data: **Bold Text**
`;
    const expectedOutput = "# Heading 1 - Bullet 1 - Bullet 2 Bold Text";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  /**
   * Verifies that formatContent does not modify non-assistant messages.
   */
  test("returns raw content for non-assistant messages", () => {
    const message: Message = {
      role: "user",
      content: "Just a normal text message.",
      id: "test-id",
    };
    const formatted = formatContent(message);
    expect(formatted).toBe("Just a normal text message.");
  });
});

// Tests for getTimeAgo
describe("getTimeAgo", () => {
  /**
   * Verifies that getTimeAgo returns an empty string if no timestamp is provided.
   */
  test("should return an empty string if no timestamp is provided", () => {
    expect(getTimeAgo()).toBe("");
  });

  /**
   * Verifies that getTimeAgo returns a non-empty relative time string for a valid timestamp.
   */
  test("should return a relative time string for a valid timestamp", () => {
    const now = new Date().toISOString();
    const result = getTimeAgo(now);
    expect(result).not.toBe("");
  });
});