/**
 * @fileoverview Unit test for parseSseData to ensure that raw markdown syntax is preserved.
 */
import { parseSseData } from "../../utils/parse-sse-data";

describe("parseSseData (raw markdown)", () => {
  it("preserves markdown bold markers and removes unnecessary spaces", () => {
    const sseInput = `
data: # Great Choice!
data: **Historical Fiction** is a rich and diverse genre, full of suspense, twists, and heart-p ounding moments.
data: Here are some gripping recommendations:
data: - "The Anime Encyclopedia: A Guide to Japanese Animation Since 1917" by Jonathan Clem ents and Helen McCarthy
data: - "Anime from Akira to Howl's Moving Castle: Exper iencing Contemporary Japanese Animation" by Susan J. Napier
data: - **The M
data: anga Artist 's Workbook** by Christopher Hart
data: Let me know if you'd like more recommendations!
`;
    const expectedMarkdown =
      '# Great Choice! **Historical Fiction** is a rich and diverse genre, full of suspense, twists, and heart-pounding moments. Here are some gripping recommendations: - "The Anime Encyclopedia: A Guide to Japanese Animation Since 1917" by Jonathan Clem ents and Helen McCarthy - "Anime from Akira to Howl\'s Moving Castle: Exper iencing Contemporary Japanese Animation" by Susan J. Napier - **The Manga Artist\'s Workbook** by Christopher Hart Let me know if you\'d like more recommendations!';

    expect(parseSseData(sseInput)).toBe(expectedMarkdown);
  });
});
