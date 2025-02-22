import type { Message } from "@ai-sdk/react";
import { formatDistanceToNow } from "date-fns";

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

  // Basic cleanup before post-processing.
  result = result.replace(/\*\*/g, "");
  result = result.replace(/\s+([,.!?;:])/g, "$1");
  result = result.replace(/([,.!?;:])(?=[^\s])/g, "$1 ");
  result = result.replace(/"\s+/g, '"').replace(/\s+"/g, '"');

  // Apply additional post-processing to collapse intra-word spaces.
  result = postProcess(result);

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
 * Joins an array of tokens into a single string using a single space, with special handling for punctuation.
 *
 * If a token consists solely of punctuation (like "!" or "."),
 * it is concatenated directly to the previous token without an extra space.
 *
 * @param {string[]} tokens - An array of cleaned tokens.
 * @returns {string} The concatenated string with normalized whitespace and correct punctuation spacing.
 */
export function joinTokens(tokens: string[]): string {
  return tokens.reduce((acc, token, index) => {
    if (index === 0) return token;
    // If token is solely punctuation, join it without a space.
    if (/^[,.!?;:]$/.test(token)) {
      return acc + token;
    }
    return acc + " " + token;
  }, "").replace(/\s+/g, " ").trim();
}

/**
 * Post-processes the text by removing markdown bold markers and cleaning up extra spaces
 * around punctuation, quotes, and within words that have been unintentionally split.
 *
 * This function performs the following steps:
 * 1. Removes any markdown bold markers (e.g., **Bold** becomes Bold).
 * 2. Removes extra spaces before punctuation and ensures exactly one space after punctuation.
 * 3. Removes extra spaces around quotes.
 * 4. Collapses intra-word spaces only when there are two or more consecutive spaces,
 *    so that "This  is formatted" becomes "This is formatted" but "This is formatted" remains unchanged.
 *
 * @param {string} text - The text to clean.
 * @returns {string} The cleaned text.
 */
export function postProcess(text: string): string {
  let result = text;
  
  // 1. Remove markdown bold markers.
  result = result.replace(/\*\*/g, "");
  
  // 2. Clean up spaces before punctuation marks and ensure one space after punctuation.
  result = result.replace(/\s+([,.!?;:])/g, "$1");
  result = result.replace(/([,.!?;:])(?=[^\s])/g, "$1 ");
  
  // 3. Remove extra spaces around quotes.
  result = result.replace(/"\s+/g, '"').replace(/\s+"/g, '"');
  
  // 4. Collapse extra intra-word spaces only if there are 2 or more spaces.
  // Replace two or more spaces between letter groups with a single space.
  result = result.replace(/([a-zA-Z]+)\s{2,}([a-zA-Z]+)/g, "$1 $2");
  
  return result;
}