/**
 * @fileoverview Unit tests for the SSE parsing and formatting functions.
 *
 * These tests verify that our helper functions produce a clean, readable markdown string.
 * The current behavior is to join all tokens with a single space and collapse extra whitespace.
 */

import {  formatContent } from "../../utils/parse-sse-data";
import type { Message } from "@ai-sdk/react";

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
