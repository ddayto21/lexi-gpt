/**
 * @fileoverview Unit tests for the SSE parsing and formatting functions.
 *
 * These tests verify that our helper functions produce a clean, readable markdown string.
 * The current behavior is to join all tokens with a single space and collapse extra whitespace.
 */

import { parseSseData, formatContent } from "../../utils/parse-sse-data";
import type { Message } from "@ai-sdk/react";

// ----------------- Tests for formatContent -----------------
describe("formatContent", () => {
  /**
   * Verifies that formatContent processes an assistant message by parsing its SSE data
   * and returning the cleaned content.
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
   * Verifies that formatContent formats bullet lists and headings correctly.
   * The expected output is a single line with tokens separated by a single space.
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
   * Verifies that non-assistant messages are not processed and remain unchanged.
   */
  test("returns raw content for non-assistant messages", () => {
    const message: Message = {
      role: "user",
      content: "Just a normal text message.",
      id: "test-id",
    };
    expect(formatContent(message)).toBe("Just a normal text message.");
  });
});
