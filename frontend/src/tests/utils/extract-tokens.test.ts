/**
 * @fileoverview Unit tests for the extractTokens function.
 *
 * These tests verify that extractTokens:
 * - Splits the input string into individual lines.
 * - Filters only lines that start with "data:".
 * - Removes the "data:" prefix and extra whitespace.
 * - Parses JSON content if the token is in JSON format.
 * - Returns an array of non-empty tokens.
 */

import { extractTokens } from "../../utils/parse-sse-data";

describe("extractTokens", () => {
  /**
   * Test that extractTokens correctly extracts tokens from a basic SSE input.
   * Input lines that start with "data:" should have the prefix removed and be returned as tokens.
   */
  test("should extract tokens from basic SSE input", () => {
    const input = `data: Hello\n\ndata: World\n\n`;
    const expected = ["Hello", "World"];
    expect(extractTokens(input)).toEqual(expected);
  });

  /**
   * Test that extractTokens parses JSON content correctly.
   * When a token is a JSON string (e.g. '{"content": "Parsed JSON"}'),
   * the function should parse it and return the value of the "content" field.
   */
  test("should parse JSON tokens correctly", () => {
    const jsonContent = JSON.stringify({ content: "Parsed JSON" });
    const input = `data: ${jsonContent}\n\n`;
    const expected = ["Parsed JSON"];
    expect(extractTokens(input)).toEqual(expected);
  });

  /**
   * Test that extractTokens ignores lines that do not start with "data:".
   * Only lines with the "data:" prefix should be returned.
   */
  test("should ignore lines that do not start with 'data:'", () => {
    const input = `random: Not included\ndata: Included\n\n`;
    const expected = ["Included"];
    expect(extractTokens(input)).toEqual(expected);
  });

  /**
   * Test that extractTokens filters out tokens that are empty after trimming.
   * Input with extra blank lines or whitespace-only tokens should result in an empty array.
   */
  test("should return an empty array for empty or whitespace-only input", () => {
    expect(extractTokens("")).toEqual([]);
    expect(extractTokens("  \n\n ")).toEqual([]);
  });

  /**
   * Test that extractTokens properly trims extra spaces from the token.
   */
  test("should trim extra whitespace from tokens", () => {
    const input = `data:    Trimmed Token   \n\n`;
    const expected = ["Trimmed Token"];
    expect(extractTokens(input)).toEqual(expected);
  });
});