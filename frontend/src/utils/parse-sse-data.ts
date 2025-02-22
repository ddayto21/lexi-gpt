import type { Message } from "@ai-sdk/react";
import { formatDistanceToNow } from "date-fns";

/**
 * Extracts and cleans SSE tokens from the input string.
 *
 * Each token is a line that starts with "data:".
 * This function removes the prefix and trims each token.
 *
 * @param {string} sseText - The raw SSE text input.
 * @returns {string[]} An array of cleaned tokens.
 */
export function extractTokens(sseText: string): string[] {
  return sseText
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("data:"))
    .map((line) => {
      const rawContent = line.replace(/^data:\s*/, "").trim();
      if (rawContent.startsWith("{") || rawContent.startsWith("[")) {
        try {
          const parsed = JSON.parse(rawContent);
          return parsed.content || "";
        } catch (err) {
          console.error("Error parsing SSE chunk as JSON:", err);
          return "";
        }
      }
      return rawContent;
    })
    .filter((token) => token.length > 0);
}

/**
 * Joins an array of tokens into a single string using a single space.
 *
 * @param {string[]} tokens - An array of tokens.
 * @returns {string} A single concatenated string.
 */
export function joinTokens(tokens: string[]): string {
  // Simply join with a space and then normalize whitespace.
  return tokens.join(" ").replace(/\s+/g, " ").trim();
}

/**
 * Parses a string containing SSE formatted data and returns a cleaned, human-readable string.
 *
 * This function extracts tokens using extractTokens() and then joins them using joinTokens().
 * It also performs additional cleanup for punctuation and quotes.
 *
 * @param {string} sseText - The raw SSE text input containing one or more SSE events.
 * @returns {string} The cleaned and concatenated content.
 */
export function parseSseData(sseText: string): string {
  if (typeof sseText !== "string") {
    throw new Error("Input must be a string");
  }
  const tokens = extractTokens(sseText);
  let result = joinTokens(tokens);

  // Remove markdown bold markers (e.g., **Bold** -> Bold)
  result = result.replace(/\*\*/g, "");

  // Additional cleanup:
  result = result.replace(/\s+([,.!?;:])/g, "$1");
  result = result.replace(/([,.!?;:])(?=[^\s])/g, "$1 ");
  result = result.replace(/"\s+/g, '"').replace(/\s+"/g, '"');

  return result;
}

/**
 * Formats the content of a chat message for display in the chat window.
 *
 * If the message is from the assistant and contains SSE data (starting with "data:"),
 * the function parses the data and returns the cleaned content.
 *
 * @param {Message} message - The chat message object.
 * @returns {string} The formatted content.
 */
export function formatContent(message: Message): string {
  if (message.role === "assistant" && typeof message.content === "string") {
    const trimmedContent = message.content.trim();
    if (trimmedContent.startsWith("data:")) {
      return parseSseData(trimmedContent);
    }
  }
  return message.content ? String(message.content) : "";
}
/**
 * Returns a human-readable string indicating how long ago the timestamp occurred.
 *
 * @param {string} [timestamp] - The timestamp string.
 * @returns {string} The relative time (e.g., "2 hours ago").
 */
export function getTimeAgo(timestamp?: string): string {
  if (!timestamp) return "";
  const dateObj = new Date(timestamp);
  return isNaN(dateObj.getTime())
    ? ""
    : formatDistanceToNow(dateObj, { addSuffix: true });
}
