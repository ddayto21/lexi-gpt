import { describe, it, expect } from "@jest/globals";
import { constructSubjectQuery } from "../open-library-api/util";

describe("constructSubjectQuery", () => {
  it("should construct a valid query string with one subject", () => {
    const result = constructSubjectQuery(["travel"]);

    const expected =
      "https://openlibrary.org/search.json?q=subject:travel&page=1&limit=10";

    expect(result).toBe(expected);
  });

  it("should construct a valid query string with multiple subjects using AND", () => {
    const result = constructSubjectQuery(["travel", "dogs"]);
    const expected =
      "https://openlibrary.org/search.json?q=subject:travel+AND+subject:dogs&page=1&limit=10";
    expect(result).toBe(expected);
  });

  it("should construct a valid query string with multiple subjects using OR", () => {
    const result = constructSubjectQuery(["travel", "dogs"], "OR");
    const expected =
      "https://openlibrary.org/search.json?q=subject:travel+OR+subject:dogs&page=1&limit=10";
    expect(result).toBe(expected);
  });

  it("should construct a query string with custom pagination values", () => {
    const result = constructSubjectQuery(["fiction"], "AND", 2, 20);
    const expected =
      "https://openlibrary.org/search.json?q=subject:fiction&page=2&limit=20";
    expect(result).toBe(expected);
  });

  it("should encode special characters in subjects", () => {
    const result = constructSubjectQuery(["Urban Fantasy", "Sci-Fi"]);
    const expected =
      "https://openlibrary.org/search.json?q=subject:Urban%20Fantasy+AND+subject:Sci-Fi&page=1&limit=10";
    expect(result).toBe(expected);
  });

  it("should throw an error if subjects array is empty", () => {
    expect(() => constructSubjectQuery([])).toThrowError(
      "At least one subject must be provided."
    );
  });
});
