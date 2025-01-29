import { submitBookSearchRequest } from "./submit-book-search-request";
import { describe, it, expect } from "@jest/globals";

describe("submitBookSearchRequest (Integration Test)", () => {
  it("should return valid results for a single word input", async () => {
    const result = await submitBookSearchRequest("travel");

    expect(result).toHaveProperty("docs");
    expect(Array.isArray(result.docs)).toBe(true);
    expect(result.docs.length).toBeGreaterThan(0);
  });

  it("should return valid results for multiple words input", async () => {
    const result = await submitBookSearchRequest("history adventure science");

    expect(result).toHaveProperty("docs");
    expect(Array.isArray(result.docs)).toBe(true);
  });

  it("should handle input with multiple spaces", async () => {
    const result = await submitBookSearchRequest("  history    science   adventure  ");

    expect(result).toHaveProperty("docs");
    expect(Array.isArray(result.docs)).toBe(true);
  });

  it("should return different results for different inputs", async () => {
    const result1 = await submitBookSearchRequest("philosophy");
    const result2 = await submitBookSearchRequest("fiction");

    expect(result1).not.toEqual(result2);
  });

  it("should handle pagination correctly", async () => {
    const resultPage1 = await submitBookSearchRequest("fiction", "AND", 1, 5);
    const resultPage2 = await submitBookSearchRequest("fiction", "AND", 2, 5);

    expect(resultPage1).toHaveProperty("docs");
    expect(resultPage2).toHaveProperty("docs");
    expect(resultPage1.docs).not.toEqual(resultPage2.docs);
  });

  it("should throw an error when the input string is empty", async () => {
    await expect(submitBookSearchRequest("")).rejects.toThrow(
      "Please enter at least one valid subject."
    );
  });

  it("should throw an error when the input string has only spaces", async () => {
    await expect(submitBookSearchRequest("   ")).rejects.toThrow(
      "Please enter at least one valid subject."
    );
  });
});