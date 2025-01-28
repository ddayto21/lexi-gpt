import { describe, it, expect } from "@jest/globals";
import { handleSearchRequest } from "./construct-subject-query";

describe("handleSearchRequest (Integration Test)", () => {
  it("should return valid results for a single subject", async () => {
    const subjects = ["travel"];
    const result = await handleSearchRequest(subjects);

    expect(result).toHaveProperty("docs");
    expect(Array.isArray(result.docs)).toBe(true);
    expect(result.docs.length).toBeGreaterThan(0);
  });

  it("should return valid results for multiple subjects with AND operator", async () => {
    const subjects = ["history", "adventure"];
    const result = await handleSearchRequest(subjects, "AND");

    expect(result).toHaveProperty("docs");
    expect(Array.isArray(result.docs)).toBe(true);
  });

  it("should return valid results for multiple subjects with OR operator", async () => {
    const subjects = ["science", "philosophy"];
    const result = await handleSearchRequest(subjects, "OR");

    expect(result).toHaveProperty("docs");
    expect(Array.isArray(result.docs)).toBe(true);
  });

  it("should handle pagination correctly", async () => {
    const subjects = ["fiction"];
    const result = await handleSearchRequest(subjects, "AND", 2, 5);

    expect(result).toHaveProperty("docs");
    expect(Array.isArray(result.docs)).toBe(true);
  });

  it("should throw an error when no subjects are provided", async () => {
    await expect(handleSearchRequest([])).rejects.toThrow(
      "Please enter at least one subject."
    );
  });
});
