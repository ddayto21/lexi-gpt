/**
 * @fileoverview Unit tests for the removeSpacesAfterHyphens function.
 *
 * These tests verify that the function correctly removes extra spaces immediately
 * following a hyphen in a word.
 */

import { removeSpacesAfterHyphens } from "../../utils/remove-spaces-after-hyphens";

describe("removeSpacesAfterHyphens", () => {
  it("removes extra spaces after a hyphen in a single occurrence", () => {
    const input = "heart-p ounding";
    const expected = "heart-pounding";
    expect(removeSpacesAfterHyphens(input)).toBe(expected);
  });

  it("removes multiple spaces after a hyphen", () => {
    const input = "well-   known";
    const expected = "well-known";
    expect(removeSpacesAfterHyphens(input)).toBe(expected);
  });

  it("does not alter text when there is no extra space after a hyphen", () => {
    const input = "quick-fix";
    const expected = "quick-fix";
    expect(removeSpacesAfterHyphens(input)).toBe(expected);
  });

  it("handles multiple hyphen occurrences in the same string", () => {
    const input = "heart-p ounding and mind-  blowing";
    const expected = "heart-pounding and mind-blowing";
    expect(removeSpacesAfterHyphens(input)).toBe(expected);
  });

  it("returns the same string if there is no hyphen", () => {
    const input = "no hyphen here";
    const expected = "no hyphen here";
    expect(removeSpacesAfterHyphens(input)).toBe(expected);
  });
});