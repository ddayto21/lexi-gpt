/**
 * @fileoverview Unit tests for punctuation and quote cleanup helper functions.
 *
 * These tests verify that:
 * - cleanPunctuation removes extra spaces before punctuation and ensures one space after punctuation.
 * - cleanQuotes removes extra spaces inside double quotes.
 */

import { cleanPunctuation, cleanQuotes } from "../../utils/parse-sse-data";

describe("cleanPunctuation", () => {
  it("removes extra spaces before punctuation and ensures one space after punctuation", () => {
    const input = "Hello   ,   World   !How are you?";
    const expected = "Hello, World! How are you?";
    expect(cleanPunctuation(input)).toBe(expected);
  });

  it("adds a space after punctuation if missing", () => {
    const input = "Hello,World";
    const expected = "Hello, World";
    expect(cleanPunctuation(input)).toBe(expected);
  });

  it("does not add extra space if punctuation is at the end of the line", () => {
    const input = "Hello, World!";
    const expected = "Hello, World!";
    expect(cleanPunctuation(input)).toBe(expected);
  });
});

describe("cleanQuotes", () => {
  it("removes extra spaces immediately inside quotes", () => {
    const input = 'She said , " hello "';
    const expected = 'She said , "hello"';
    expect(cleanQuotes(input)).toBe(expected);
  });

  it("handles multiple quoted sections", () => {
    const input = '"  Hello " and " World "';
    const expected = '"Hello" and "World"';
    expect(cleanQuotes(input)).toBe(expected);
  });
});