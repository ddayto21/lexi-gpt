import { searchBooks, getBookCover } from "./client";
import { beforeAll, jest, describe, it, expect } from "@jest/globals";

describe.skip("Open Library API - Book Search (Integration Tests)", () => {
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

describe("Book Cover URLs", () => {
  it("should generate a valid medium-sized book cover URL", () => {
    const olid = "OL12345M";
    const size = "M";
    const result = getBookCover(olid, size);
    const expectedUrl = `https://covers.openlibrary.org/b/olid/${olid}-${size}.jpg`;

    expect(result).toBe(expectedUrl);
    expect(result).toMatch(
      /^https:\/\/covers\.openlibrary\.org\/b\/olid\/OL\d+M-[SML]\.jpg$/
    );
  });

  it("should default to medium size when no size is provided", () => {
    const olid = "OL67890M";
    const result = getBookCover(olid);
    const expectedUrl = `https://covers.openlibrary.org/b/olid/${olid}-M.jpg`;

    expect(result).toBe(expectedUrl);
  });

  it("should generate a valid small-sized book cover URL", () => {
    const olid = "OL98765M";
    const size = "S";
    const result = getBookCover(olid, size);
    const expectedUrl = `https://covers.openlibrary.org/b/olid/${olid}-${size}.jpg`;

    expect(result).toBe(expectedUrl);
  });

  it("should generate a valid large-sized book cover URL", () => {
    const olid = "OL13579M";
    const size = "L";
    const result = getBookCover(olid, size);
    const expectedUrl = `https://covers.openlibrary.org/b/olid/${olid}-${size}.jpg`;

    expect(result).toBe(expectedUrl);
  });

  it("should handle invalid OLID gracefully", () => {
    const olid = ""; // Empty OLID
    const size = "M";
    const result = getBookCover(olid, size);
    const expectedUrl = "https://covers.openlibrary.org/b/olid/-M.jpg";

    expect(result).toBe(expectedUrl);
  });
});
