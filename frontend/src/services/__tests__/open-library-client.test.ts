import { searchBooks } from "../open-library-client";
import { describe, it, expect } from "@jest/globals";

describe("Open Library (Book) API integration", () => {
  it("should return valid book search results from Open Library", async () => {
    const result = await searchBooks("The Lord of the Rings");
    console.log(`result: ${JSON.stringify(result, null, 2)}`);
    expect(result).toHaveProperty("start");
    expect(result).toHaveProperty("num_found");
    expect(Array.isArray(result.docs)).toBe(true);
    expect(result.docs.length).toBeGreaterThan(0);

    const firstBook = result.docs[0];
    expect(firstBook).toHaveProperty("title");
    expect(firstBook).toHaveProperty("key");
  });

  it("should return an empty result set for an unlikely search query", async () => {
    const result = await searchBooks("ajsdnfoqweirjlzxcmn1234");

    expect(result).toHaveProperty("start");
    expect(result).toHaveProperty("num_found");
    expect(Array.isArray(result.docs)).toBe(true);
    expect(result.docs.length).toBe(0);
  });
});
