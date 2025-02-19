import type { Message } from "@ai-sdk/react";
import { formatDistanceToNow } from "date-fns";

/**
 * Parses a string containing SSE (Server-Sent Event) formatted data and returns
 * a human-readable string by concatenating the data payloads, even if there are multiple 'data:' in one line.
 *
 * @param {string} sseText - The raw SSE text input containing one or more SSE events.
 * @returns {string} A human-readable string formed by concatenating the data payloads from the SSE events.
 */
export function parseSseData(sseText: string): string {
  if (typeof sseText !== "string") {
    throw new Error("Input must be a string");
  }

  // Split by newline and then by 'data:' within each line
  const dataLines = sseText
    .split("\n")
    .flatMap((line) => {
      // Only process lines starting with 'data:'
      if (line.trim().startsWith("data:")) {
        return line.split(/data:\s*/).filter((part) => part.trim() !== "");
      }
      return []; // Return empty array for lines not starting with 'data:'
    })
    .map((part) => part.trim())
    // Remove any empty strings that might result from multiple 'data:' without content
    .filter(Boolean);

  // Join all parts into a single string
  return dataLines.join(" ");
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
