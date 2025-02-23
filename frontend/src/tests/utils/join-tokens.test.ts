import { joinTokens } from "../../utils/parse-sse-data";


describe("joinTokens", () => {
  test("should join tokens with a single space", () => {
    const tokens = ["Hello", "World"];
    const expected = "Hello World";
    expect(joinTokens(tokens)).toBe(expected);
  });

  test("should collapse extra whitespace between tokens", () => {
    const tokens = ["Hello", "   World  "];
    const expected = "Hello World";
    expect(joinTokens(tokens)).toBe(expected);
  });

  test("should join multiple tokens intelligently, collapsing intra-word spaces when needed", () => {
    const tokens = ["The", "M", "anga", "Artist", "'s", "Workbook"];
    const expected = "The Manga Artist's Workbook";
    expect(joinTokens(tokens)).toBe(expected);
  });
});
