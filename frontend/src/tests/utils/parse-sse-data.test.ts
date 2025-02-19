import { parseSseData, formatContent } from "../../utils/parse-sse-data";
import type { Message } from "@ai-sdk/react";

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

  it("should handle multiple data lines", () => {
    expect(parseSseData("data: Hello\ndata: World!\n\n")).toBe("Hello World!");
  });

  it("should return empty string for no data", () => {
    expect(parseSseData("")).toBe("");
    expect(parseSseData("  \n\n ")).toBe("");
  });

  it("should throw error on invalid input", () => {
    expect(() => parseSseData(null as unknown as string)).toThrow("Input must be a string");
  });

  it("formatContent works with assistant messages", () => {
    const message: Message = {
      role: "assistant",
      content: "data: This is formatted\n",
      id: "some-unique-id"
    };
    expect(formatContent(message)).toBe("This is formatted");
  });
});
