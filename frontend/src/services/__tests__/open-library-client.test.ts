import { searchBooks } from "../open-library-client";
import { beforeAll, jest, describe, it, expect } from "@jest/globals";

describe("Book Search (Integration Test)", () => {
  beforeAll(() => {
    jest.setTimeout(15000); // Extend timeout for slow API responses
  });

  it("should return valid book search results from Open Library", async () => {
    const result = await searchBooks("The Lord of the Rings");

    expect(result).toHaveProperty("start");
    expect(result).toHaveProperty("num_found");
    expect(Array.isArray(result.docs)).toBe(true);
    expect(result.docs.length).toBeGreaterThan(0);

    const firstBook = result.docs[0];
    expect(firstBook).toHaveProperty("title");
    expect(typeof firstBook.title).toBe("string");
    expect(firstBook).toHaveProperty("key");
    expect(firstBook).toHaveProperty("author_name");
  });

  it("should return an empty result set for an unlikely search query", async () => {
    const result = await searchBooks("ajsdnfoqweirjlzxcmn1234");

    console.log("Empty search response:", JSON.stringify(result, null, 2)); // Debugging log

    expect(result).toHaveProperty("start");
    expect(result).toHaveProperty("num_found");
    expect(Array.isArray(result.docs)).toBe(true);
    expect(result.docs.length).toBe(0);
  });

  it("should handle API errors gracefully", async () => {
    await expect(searchBooks("")).rejects.toThrow("Query cannot be empty.");
  });
});
