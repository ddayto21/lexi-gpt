import { processSearchForm } from "./process-search-form"
import { describe, it, expect } from "@jest/globals";

describe("processSearchForm", () => {
  it("should split a single word input into an array", () => {
    const result = processSearchForm("travel");
    expect(result).toEqual(["travel"]);
  });

  it("should split a multi-word input into an array of words", () => {
    const result = processSearchForm("history science adventure");
    expect(result).toEqual(["history", "science", "adventure"]);
  });

  it("should handle extra spaces between words", () => {
    const result = processSearchForm("   history    science   adventure  ");
    expect(result).toEqual(["history", "science", "adventure"]);
  });

  it("should handle leading and trailing spaces", () => {
    const result = processSearchForm("  history  ");
    expect(result).toEqual(["history"]);
  });

  it("should throw an error for an empty input string", () => {
    expect(() => processSearchForm("")).toThrow(
      "Please enter at least one valid subject."
    );
  });

  it("should throw an error for a string with only spaces", () => {
    expect(() => processSearchForm("      ")).toThrow(
      "Please enter at least one valid subject."
    );
  });
});