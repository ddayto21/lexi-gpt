/**
 * @fileoverview Unit tests for the extractTokens function.
 *
 * These tests verify that extractTokens:
 * - Splits the input string into individual lines.
 * - Removes the "data:" prefix if present.
 * - Parses JSON content if the token is in JSON format.
 * - Preserves lines even if they do not start with "data:".
 * - Returns an array of non-empty tokens.
 */

import { extractTokens } from "../../utils/parse-sse-data";

describe("extractTokens", () => {
  test("should extract tokens from basic SSE input", () => {
    const input = `data: Hello\n\ndata: World\n\n`;
    const expected = ["Hello", "World"];
    expect(extractTokens(input)).toEqual(expected);
  });

  test("should parse JSON tokens correctly", () => {
    const jsonContent = JSON.stringify({ content: "Parsed JSON" });
    const input = `data: ${jsonContent}\n\n`;
    const expected = ["Parsed JSON"];
    expect(extractTokens(input)).toEqual(expected);
  });

  test("should include lines that do not start with 'data:'", () => {
    const input = `random: keep me\ndata: This is SSE\nno prefix here\n\n`;
    // Explanation:
    // - "random: keep me" => remain as is
    // - "data: This is SSE" => "This is SSE"
    // - "no prefix here" => remain as is
    // - blank line => removed
    const expected = ["random: keep me", "This is SSE", "no prefix here"];
    expect(extractTokens(input)).toEqual(expected);
  });

  test("should return an empty array for empty or whitespace-only input", () => {
    expect(extractTokens("")).toEqual([]);
    expect(extractTokens("  \n\n ")).toEqual([]);
  });

  test("should trim extra whitespace from tokens", () => {
    const input = `data:    Trimmed Token   \n\n`;
    const expected = ["Trimmed Token"];
    expect(extractTokens(input)).toEqual(expected);
  });
});