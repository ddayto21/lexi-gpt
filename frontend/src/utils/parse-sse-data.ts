/**
 * Parses a string containing SSE (Server-Sent Event) formatted data and returns
 * a human-readable string by concatenating the data payloads.
 *
 * The function splits the input text by newlines, filters out the lines that start
 * with "data:" (ignoring any leading/trailing whitespace), removes the "data:" prefix
 * along with any whitespace following it, and then joins the remaining strings with a space.
 *
 * @param {string} sseText - The raw SSE text input containing one or more SSE events.
 * @returns {string} A human-readable string formed by concatenating the data payloads from the SSE events.
 *
 */

export function parseSseData(sseText: string): string {
  return sseText
    .split("\n")
    .filter((line) => line.trim().startsWith("data:"))
    .map((line) => line.replace(/^data:\s*/, ""))
    .join(" ");
}
