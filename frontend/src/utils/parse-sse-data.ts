import type { Message } from "@ai-sdk/react";
import { formatDistanceToNow } from "date-fns";

/**
 * Parses a string containing SSE formatted data and returns a human-readable string.
 * If the text after "data:" is valid JSON with a "content" field, it extracts that field.
 * Otherwise, it treats the remainder as plain text.
 *
 * @param {string} sseText - The raw SSE text input containing one or more SSE events.
 * @returns {string} The concatenated content from all SSE events.
 */
export function parseSseData(sseText: string): string {
  console.log("sseText:", sseText);
  if (typeof sseText !== "string") {
    throw new Error("Input must be a string");
  }

  // Split the text by newlines and filter only lines that start with "data:"
  const dataLines = sseText.split("\n").filter((line) => line.startsWith("data:"));

  const contentParts = dataLines.map((line) => {
    // Remove the "data:" prefix and trim whitespace
    const rawContent = line.replace(/^data:\s*/, "").trim();
    
    // If the raw content looks like JSON (starts with "{" or "["), try to parse it.
    if (rawContent.startsWith("{") || rawContent.startsWith("[")) {
      try {
        const parsed = JSON.parse(rawContent);
        return parsed.content || "";
      } catch (err) {
        console.error("Error parsing SSE chunk as JSON:", err);
        return "";
      }
    } else {
      // Otherwise, return the raw text.
      return rawContent;
    }
  });

  // Join the content parts with a space
  return contentParts.join(" ");
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
