/**
 * @fileoverview Unit tests for the postProcess function.
 *
 * These tests verify that postProcess correctly:
 * 1. Removes extra spaces before punctuation and ensures exactly one space after punctuation.
 * 2. Collapses multiple spaces into a single space.
 * 3. Removes extra spaces immediately inside double quotes.
 * 4. Removes unwanted spaces between a word and an apostrophe followed by "s".
 */

import { postProcess } from "../../utils/parse-sse-data";

describe("postProcess", () => {
  /**
   * Test that extra spaces before punctuation are removed and exactly one space follows punctuation.
   *
   * Example:
   * Input: "Hello   ,   World   !How are you?"
   * Expected Output: "Hello, World! How are you?"
   */
  it("removes extra spaces before punctuation and ensures one space after punctuation", () => {
    const input = "Hello   ,   World   !How are you?";
    const expected = "Hello, World! How are you?";
    expect(postProcess(input)).toBe(expected);
  });

  /**
   * Test that multiple consecutive spaces are collapsed to a single space.
   *
   * Example:
   * Input: "This    is   formatted"
   * Expected Output: "This is formatted"
   */
  it("collapses multiple spaces into a single space", () => {
    const input = "This    is   formatted";
    const expected = "This is formatted";
    expect(postProcess(input)).toBe(expected);
  });

  /**
   * Test that extra spaces inside quotes are removed.
   *
   * Example:
   * Input: 'She said, "  hello  "'
   * Expected Output: 'She said, "hello"'
   */
  it("removes extra spaces immediately inside quotes", () => {
    const input = 'She said, "  hello  "';
    const expected = 'She said, "hello"';
    expect(postProcess(input)).toBe(expected);
  });

  /**
   * Test that any unwanted space between a word and an apostrophe followed by "s" is removed.
   *
   * Example:
   * Input: "Artist 's"
   * Expected Output: "Artist's"
   */
  it("removes unwanted space before an apostrophe-s", () => {
    const input = "Artist 's";
    const expected = "Artist's";
    expect(postProcess(input)).toBe(expected);
  });
  it("removes extra spaces immediately following a hyphen in a hyphenated word", () => {
    const input = "heart-p ounding";
    const expected = "heart-pounding";
    expect(postProcess(input)).toBe(expected);
  });

  it("handles a complex example with punctuation, quotes, and apostrophe-s", () => {
    const input = '  **Bold  Text**   ,   "  extra   quoted  " and Artist \' s';
    const expected = '**Bold Text**, "extra quoted" and Artist\'s';
    expect(postProcess(input)).toBe(expected);
  });
  
});
