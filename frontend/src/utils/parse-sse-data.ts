import type { Message } from "@ai-sdk/react";
import { formatDistanceToNow } from "date-fns";

/* ------------------------------------------------------------------
 *                   High-Level Orchestrator
 * ------------------------------------------------------------------ */

/**
 * Parses a string containing SSE-formatted data and returns a cleaned, Markdown-friendly string.
 *
 * Overall steps:
 * 1. Validate input is a string.
 * 2. Extract tokens using extractTokens().
 * 3. Join tokens with joinTokens(), which preserves markdown markers intelligently.
 * 4. Clean punctuation and quotes.
 * 5. Post-process any leftover spacing issues.
 *
 * @param {string} sseText - The raw SSE text with SSE events.
 * @returns {string} - The cleaned and concatenated markdown content.
 * @throws {Error} If the input is not a string.
 */
export function parseSseData(sseText: string): string {
  validateSseInput(sseText);

  // 2) Extract tokens (SSE lines, possibly JSON lines)
  const tokens = extractTokens(sseText);

  // 3) Join tokens with intelligent spacing (for Markdown)
  let result = joinTokens(tokens);

  // 4) Clean punctuation/spaces + quotes
  result = cleanPunctuation(result);
  result = cleanQuotes(result);

  // 5) Final post-processing (collapsing hyphens, etc.)
  result = postProcess(result);

  return result;
}

/* ------------------------------------------------------------------
 *                   Helper: Validate SSE Input
 * ------------------------------------------------------------------ */

function validateSseInput(sseText: unknown): asserts sseText is string {
  if (typeof sseText !== "string") {
    throw new Error("parseSseData input must be a string.");
  }
}

/* ------------------------------------------------------------------
 *                   Helper: Extract Tokens
 * ------------------------------------------------------------------ */

/**
 * Extracts tokens from the given SSE text:
 * 1) Split by newlines.
 * 2) If a line starts with "data:", remove that prefix.
 * 3) Trim each line.
 * 4) If the line is valid JSON ({...} or [...]), parse and return parsed.content.
 * 5) Filter out any empty lines.
 *
 * @param {string} sseText - The full SSE text.
 * @returns {string[]} An array of extracted content tokens.
 */
export function extractTokens(sseText: string): string[] {
  return (
    sseText
      // (1) Split by newlines (support both \r\n and \n)
      .split(/\r?\n/)
      // (2) Strip "data:" prefix if present
      .map((line) => {
        if (line.trimStart().startsWith("data:")) {
          return line.replace(/^(\s*)data:\s*/, "$1"); // remove data:
        }
        return line;
      })
      // (3) Trim each line
      .map((line) => line.trim())
      // (4) If JSON, parse and return `parsed.content`
      .map((rawContent) => {
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
      // (5) Remove empty tokens
      .filter((token) => token.length > 0)
  );
}

/* ------------------------------------------------------------------
 *                   Helper: Join Tokens Intelligently
 * ------------------------------------------------------------------ */

/**
 * Joins an array of tokens into a single string using a single space,
 * with "intelligent" merging that preserves Markdown syntax.
 *
 * Examples:
 * - If a token is solely punctuation, append it without a space.
 * - If a token starts with an apostrophe or markdown marker (e.g. "**"), append it directly.
 * - If the previous token is exactly 1 alphabetical character, merge them without a space
 *   (e.g., "L apple" => "Lapple" if "L" is not 'a' or 'I').
 *
 * @param {string[]} tokens - The array of tokens from SSE data.
 * @returns {string} Concatenated string with normalized spacing.
 */
export function joinTokens(tokens: string[]): string {
  return tokens
    .reduce((acc, token, index) => {
      const trimmed = token.trim();
      if (index === 0) return trimmed;

      // If token is purely punctuation, append it with no space
      if (/^[,.!?;:]$/.test(trimmed)) {
        return acc + trimmed;
      }

      // If token starts with an apostrophe or asterisks (Markdown bold), no space
      if (/^['*]/.test(trimmed)) {
        return acc + trimmed;
      }

      // Get the last word in 'acc'
      const accWords = acc.split(" ");
      const lastWord = accWords[accWords.length - 1];

      // If the last word is exactly 1 letter, we might merge
      if (
        /^[A-Za-z]$/.test(lastWord) &&
        /^[A-Za-z]/.test(trimmed) &&
        !/^[aiAI]$/.test(lastWord) // Maybe skip merging 'a' or 'I' if that's undesired
      ) {
        accWords[accWords.length - 1] = lastWord + trimmed;
        return accWords.join(" ");
      }

      // Otherwise, join with a space
      return acc + " " + trimmed;
    }, "")
    // Collapse any accidental multiple spaces
    .replace(/\s+/g, " ")
    .trim();
}

/* ------------------------------------------------------------------
 *                   Helper: Clean Punctuation
 * ------------------------------------------------------------------ */

/**
 * Cleans punctuation by removing extra spaces before punctuation,
 * and ensuring exactly one space after punctuation if not EOL.
 *
 * @param {string} text - The text to clean.
 * @returns {string} Cleaned text.
 */
export function cleanPunctuation(text: string): string {
  // Remove extra spaces before punctuation
  let result = text.replace(/\s+([,.!?;:])/g, "$1");
  // Ensure 1 space after punctuation if next char isn't space or end of line
  result = result.replace(/([,.!?;:])(?=[^\s])/g, "$1 ");
  return result.trim();
}

/* ------------------------------------------------------------------
 *                   Helper: Clean Quotes
 * ------------------------------------------------------------------ */

/**
 * Cleans up quotes in a string by removing extra spaces inside double quotes.
 * E.g. "She said , " hello "" => "She said , "hello""
 *
 * @param {string} text - The text to clean.
 * @returns {string} The cleaned text.
 */
export function cleanQuotes(text: string): string {
  return text.replace(/"([^"]*?)"/g, (_match, p1) => `"${p1.trim()}"`).trim();
}

/* ------------------------------------------------------------------
 *                   Helper: Post Process
 * ------------------------------------------------------------------ */

/**
 * Applies final transformations to the text. Typically:
 * 1) Trim text
 * 2) Remove extra spaces before punctuation
 * 3) Collapse multiple spaces
 * 4) Trim inside quotes
 * 5) Handle apostrophe + "s" spacing
 * 6) Remove extra spaces after hyphens
 */
export function postProcess(text: string): string {
  let result = text.trim();

  // Remove extra spaces before punctuation
  result = result.replace(/\s+([,.!?;:])/g, "$1");
  // Ensure a space after punctuation if next char isn't a space
  result = result.replace(/([,.!?;:])(?=[^\s])/g, "$1 ");

  // Collapse multiple spaces
  result = result.replace(/\s+/g, " ").trim();

  // Trim inside double quotes
  result = result.replace(/"([^"]*?)"/g, (_m, p1) => `"${p1.trim()}"`);

  // Remove unwanted space between a word and "'s"
  result = result.replace(/(\w)\s+(')\s*(s\b)/gi, "$1$2$3");

  // Remove extra spaces after hyphens (like "heart-p ounding" => "heart-pounding")
  // This is a simpler approach that won't remove newlines:
  result = removeSpacesAfterHyphens(result);

  return result;
}

/* ------------------------------------------------------------------
 *                   Helper: Remove Spaces After Hyphens
 * ------------------------------------------------------------------ */

/**
 * Collapses spaces after a hyphen if it's in the same word,
 * preserving line breaks (e.g. no removing newlines).
 */
export function removeSpacesAfterHyphens(text: string): string {
  return text.replace(/-[^\S\r\n]+/g, "-");
}

/* ------------------------------------------------------------------
 *                   Format Chat Content for Display
 * ------------------------------------------------------------------ */

/**
 * Formats the content of a chat message for display in the chat window.
 *
 * 1) Convert `message.content` to string safely (handles null/undefined).
 * 2) If it's an assistant message & starts with "data:", parse SSE data.
 * 3) Remove in-word hyphen spacing, preserving Markdown bullets.
 * 4) Return the final string for rendering as Markdown.
 */
export function formatContent(message: Message): string {
  // (1) Safely coerce to string
  let rawContent = message?.content != null ? String(message.content) : "";
  rawContent = rawContent.trim();

  // (2) If assistant role & starts with "data:", parse SSE data
  if (message.role === "assistant" && rawContent.startsWith("data:")) {
    rawContent = parseSseData(rawContent);
  }

  // (3) Remove spaces after in-word hyphens, preserving bullets
  rawContent = removeSpacesAfterInWordHyphen(rawContent);

  // (4) Return result
  return rawContent;
}

/**
 * Removes extra spaces that appear after a hyphen, but only if
 * a non-whitespace character precedes the hyphen.
 * (Prevents collapsing Markdown bullets like "- Bullet".)
 *
 * Example:
 *   "heart-p ounding" => "heart-pounding"
 *   leaves "\n- Bullet" intact on its own line.
 */
function removeSpacesAfterInWordHyphen(text: string): string {
  // Matches hyphen + spaces only if preceded by a non-whitespace char
  // This preserves bullet lines, e.g. "\n- My bullet" is untouched.
  return text.replace(/(?<=\S)-[^\S\r\n]+/g, "-");
}

/* ------------------------------------------------------------------
 *                   Utility: Relative Timestamp
 * ------------------------------------------------------------------ */

/**
 * Returns a human-readable string like "2 hours ago" for the given timestamp.
 */
export function getTimeAgo(timestamp?: string): string {
  if (!timestamp) return "";
  const dateObj = new Date(timestamp);
  return isNaN(dateObj.getTime())
    ? ""
    : formatDistanceToNow(dateObj, { addSuffix: true });
}