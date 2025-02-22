import type { Message } from "@ai-sdk/react";
import { formatDistanceToNow } from "date-fns";


/**
 * Parses a string containing SSE formatted data and returns a cleaned, human-readable string.
 * This version extracts text from each SSE event (either plain text or JSON with a "content" field),
 * then removes markdown formatting and applies additional formatting to remove extra spaces around
 * special characters such as punctuation, hyphens, and quotes.
 *
 * @param {string} sseText - The raw SSE text input containing one or more SSE events.
 * @returns {string} The cleaned and concatenated content from all SSE events.
 */
export function parseSseData(sseText: string): string {

  if (typeof sseText !== "string") {
    throw new Error("Input must be a string");
  }

  // Split the input into lines, trim each line, and keep only lines that start with "data:"
  const dataLines = sseText
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("data:"));

  // Extract the content from each data line. If the content is JSON, extract the 'content' field;
  // otherwise, use the plain text.
  const contentParts = dataLines.map((line) => {
    const rawContent = line.replace(/^data:\s*/, "").trim();
    if (rawContent.startsWith("{") || rawContent.startsWith("[")) {
      try {
        const parsed = JSON.parse(rawContent);
        return parsed.content || "";
      } catch (err) {
        console.error("Error parsing SSE chunk as JSON:", err);
        return "";
      }
    } else {
      return rawContent;
    }
  });

  // Join all parts together with a single space and normalize whitespace
  let result = contentParts.join(" ").replace(/\s+/g, " ").trim();

  // Remove markdown bold markers (i.e. "**") while preserving other markdown characters.
  result = result.replace(/\*\*/g, "");

  // Additional formatting to clean up spacing:
  // Remove extra spaces before punctuation marks like !, ., ,, ?, :, and ;
  result = result.replace(/\s+([,.!?;:])/g, "$1");
  // Ensure there is exactly one space after punctuation marks if not end-of-line.
  result = result.replace(/([,.!?;:])(?=[^\s])/g, "$1 ");
  // Remove extra spaces around quotes.
  result = result.replace(/"\s+/g, '"');
  result = result.replace(/\s+"/g, '"');

  return result;
}

/**
 * Formats the content of a chat message for display in the chat window.
 *
 * If the message is from the assistant and contains a string starting with "data:",
 * the function parses the SSE data and returns the human-readable content.
 *
 * @param {Message} message - The chat message object to format.
 * @returns {string} The formatted content of the chat message.
 */
export function formatContent(message: Message): string {
  if (message.role === "assistant" && typeof message.content === "string") {
    const trimmedContent = message.content.trim();
    if (trimmedContent.startsWith("data:")) {
      return parseSseData(trimmedContent);
    }
  }
  // Handle undefined or non-string content
  return message.content ? String(message.content) : "";
}

export function getTimeAgo(timestamp?: string) {
  if (!timestamp) return "";
  const dateObj = new Date(timestamp);
  return isNaN(dateObj.getTime())
    ? ""
    : formatDistanceToNow(dateObj, { addSuffix: true });
}
