import { joinTokens } from "../../utils/parse-sse-data";

// ----------------- Tests for joinTokens -----------------
describe("joinTokens", () => {
  /**
   * Verifies that joinTokens concatenates an array of tokens with a single space.
   */
  test("should join tokens with a single space", () => {
    const tokens = ["Hello", "World"];
    const expected = "Hello World";
    expect(joinTokens(tokens)).toBe(expected);
  });

  /**
   * Verifies that joinTokens collapses extra whitespace between tokens.
   */
  test("should collapse extra whitespace between tokens", () => {
    const tokens = ["Hello", "   World  "];
    const expected = "Hello World";
    expect(joinTokens(tokens)).toBe(expected);
  });

  /**
   * Verifies that joinTokens intelligently joins multiple tokens.
   * For example, ["Absolutely", "!", "Non", "-fiction", ...] should produce a readable sentence.
   */
  test("should join multiple tokens intelligently", () => {
    const tokens = [
      "Absolutely",
      "!",
      "Non",
      "-fiction",
      "is",
      "a",
      "vast",
      "and",
      "fascinating",
      "genre",
      ".",
    ];
    const expected =
      "Absolutely! Non -fiction is a vast and fascinating genre.";
    // Note: if you want "Non-fiction" (no space between Non and -fiction), adjust expected accordingly.
    expect(joinTokens(tokens)).toBe(expected);
  });
});
