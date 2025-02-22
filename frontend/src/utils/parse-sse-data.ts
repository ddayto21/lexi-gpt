import type { Message } from "@ai-sdk/react";
import { formatDistanceToNow } from "date-fns";
import { removeSpacesAfterHyphens } from "./remove-spaces-after-hyphens";
/**
 * Parses a string containing SSE formatted data and returns a cleaned markdown string.
 *
 * Steps:
 * 1. Validates that the input is a string.
 * 2. Extracts tokens using extractTokens().
 * 3. Joins tokens using joinTokens(), preserving markdown markers.
 * 4. Cleans up extra spaces around punctuation and quotes.
 * 5. Applies additional post-processing (via postProcess()) to collapse unintended intra-word spaces.
 *
 * @param {string} sseText - The raw SSE text input containing one or more SSE events.
 * @returns {string} The cleaned and concatenated markdown content.
 * @throws {Error} If the input is not a string.
 */
export function parseSseData(sseText: string): string {
  if (typeof sseText !== "string") {
    throw new Error("Input must be a string");
  }
  const tokens = extractTokens(sseText);
  let result = joinTokens(tokens);

  result = cleanPunctuation(result);
  result = cleanQuotes(result);

  result = postProcess(result);

  return result;
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
 * Joins an array of tokens into a single string using a single space,
 * with intelligent merging that preserves markdown syntax.
 *
 * This function performs the following:
 * - Trims each token.
 * - Inserts a single space between tokens by default.
 * - If a token is solely punctuation, it appends it directly without an extra space.
 * - If a token starts with an apostrophe or markdown marker (e.g. "**"), it appends it directly.
 * - If the previous token is exactly one alphabetical character (and not "a" or "I") and the current token
 *   starts with a letter, they are merged without an intervening space.
 *
 * @param {string[]} tokens - An array of cleaned tokens.
 * @returns {string} The concatenated string with normalized whitespace.
 */
export function joinTokens(tokens: string[]): string {
  return tokens
    .reduce((acc, token, index) => {
      const trimmed = token.trim();
      if (index === 0) return trimmed;

      // If token is solely punctuation, append it without a space.
      if (/^[,.!?;:]$/.test(trimmed)) {
        return acc + trimmed;
      }

      // If token starts with an apostrophe or markdown marker, append it directly.
      if (/^['*]/.test(trimmed)) {
        return acc + trimmed;
      }

      // Get the last word from the accumulated string, trimmed.
      const accWords = acc.split(" ");
      const lastWord = accWords[accWords.length - 1].trim();

      // If the last word is exactly one alphabetical character (e.g., "M") and the current token starts with a letter,
      // merge them without an extra space.
      if (
        lastWord.length === 1 &&
        /^[A-Za-z]$/.test(lastWord) &&
        /^[A-Za-z]/.test(trimmed)
      ) {
        accWords[accWords.length - 1] = lastWord + trimmed;
        return accWords.join(" ");
      }

      // Otherwise, join with a single space.
      return acc + " " + trimmed;
    }, "")
    .replace(/\s+/g, " ")
    .trim();
}
/**
 * Cleans up punctuation in a string by:
 * - Removing extra spaces before punctuation marks.
 * - Ensuring exactly one space after punctuation if not at the end of the string.
 *
 * @param {string} text - The text to clean.
 * @returns {string} The cleaned text.
 */
export function cleanPunctuation(text: string): string {
  // Remove extra spaces before punctuation.
  let result = text.replace(/\s+([,.!?;:])/g, "$1");
  // Ensure exactly one space after punctuation if not followed by a space.
  result = result.replace(/([,.!?;:])\s*/g, "$1 ");
  return result.trim();
}

/**
 * Cleans up quotes in a string by removing extra spaces inside quoted content.
 *
 * This function searches for text enclosed in double quotes and trims any
 * leading or trailing whitespace inside the quotes. For example, it converts:
 *
 *   'She said , " hello "'  --> 'She said , "hello"'
 *
 * @param {string} text - The text to clean.
 * @returns {string} The cleaned text.
 */
export function cleanQuotes(text: string): string {
  return text.replace(/"([^"]*?)"/g, (_match, p1) => `"${p1.trim()}"`).trim();
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
 * Post-processes the text by cleaning up extra spaces around punctuation, quotes,
 * and within words that have been unintentionally split.
 *
 * The function performs the following steps:
 * 1. Trims the entire text.
 * 2. Removes extra spaces before punctuation and ensures exactly one space after punctuation.
 * 3. Collapses multiple spaces into a single space.
 * 4. Trims the content inside double quotes.
 * 5. Removes any unwanted space between a word and an apostrophe followed by "s".
 * 6. Removes extra spaces after hyphens in words (e.g. "heart-p ounding" becomes "heart-pounding").
 * 
 * @param {string} text - The text to clean.
 * @returns {string} The cleaned text.
 */
export function postProcess(text: string): string {
  // 1. Trim the entire text.
  let result = text.trim();

  // 2. Remove extra spaces before punctuation marks.
  result = result.replace(/\s+([,.!?;:])/g, "$1");
  // Ensure exactly one space after punctuation if not at end-of-line.
  result = result.replace(/([,.!?;:])(?=[^\s])/g, "$1 ");

  // 3. Collapse multiple spaces into a single space.
  result = result.replace(/\s+/g, " ").trim();

  // 4. Trim the content inside double quotes.
  // This finds text between double quotes and trims any leading/trailing spaces.
  result = result.replace(/"([^"]*?)"/g, (_match, p1) => `"${p1.trim()}"`);

  // 5. Remove unwanted space between a word and an apostrophe followed by "s".
  // Matches a word character, one or more spaces, then an apostrophe, optional spaces, then "s".
  result = result.replace(/(\w)\s+(')\s*(s\b)/gi, "$1$2$3");


  // 6. Remove extra spaces immediately following a hyphen in a hyphenated word.
  result = removeSpacesAfterHyphens(result);

  return result;
}


