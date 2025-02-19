import { parseSseData } from "../../utils/parse-sse-data";

describe("parseSseData", () => {
  test("should return an empty string for empty input", () => {
    expect(parseSseData("")).toBe("");
  });

  test("should parse a single SSE event correctly", () => {
    const input = "data: Hello\n\n";
    const expectedOutput = "Hello";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  test("should parse multiple SSE events correctly", () => {
    const input = "data: Hello\n\ndata: World\n\n";
    const expectedOutput = "Hello World";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  test("should ignore lines that do not start with 'data:'", () => {
    const input = "random: Not included\ndata: Included\n";
    const expectedOutput = "Included";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  test("should handle extra spaces after 'data:'", () => {
    const input = "data:    Spaced\n\n";
    const expectedOutput = "Spaced";
    expect(parseSseData(input)).toBe(expectedOutput);
  });

  test("should concatenate events with a space", () => {
    const input = "data: Part1\n\ndata: Part2\n\ndata: Part3\n\n";
    const expectedOutput = "Part1 Part2 Part3";
    expect(parseSseData(input)).toBe(expectedOutput);
  });
});
