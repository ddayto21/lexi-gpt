/**
 * @module stream
 *
 * This module provides utility functions for processing streamed text data.
 * It includes functions to sanitize incoming text chunks by removing unwanted
 * markdown markers, concatenate chunks with proper spacing, and finalize the
 * stream buffer by detecting and removing a termination marker ("[DONE]").
 *
 * These functions are designed to facilitate parsing and formatting of streamed
 * responses in a consistent and testable manner.
 */

/**
 * Sanitizes an input chunk by removing markdown markers and extraneous whitespace.
 *
 * This function checks for common markdown markers such as "```json" at the start and "```" at the end,
 * and removes them from the provided string. It then returns the cleaned and trimmed string.
 *
 * @param {string} chunk - The raw text chunk to sanitize.
 * @returns {string} The sanitized text.
 */
export function sanitizeChunk(chunk: string): string {
  let sanitized = chunk.trim();
  if (sanitized.startsWith("```json")) {
    sanitized = sanitized.slice(7).trim();
  }
  if (sanitized.endsWith("```")) {
    sanitized = sanitized.slice(0, -3).trim();
  }
  return sanitized;
}

/**
 * Concatenates a new text chunk to an existing buffer, inserting a space if necessary.
 *
 * This function appends the provided chunk to the buffer. If the buffer does not end with a space
 * and the new chunk does not start with a space, a single space is inserted between them.
 *
 * @param {string} buffer - The current text buffer.
 * @param {string} chunk - The new text chunk to append.
 * @returns {string} The updated buffer with the chunk appended.
 */
export function concatenateChunkWithSpace(
  buffer: string,
  chunk: string
): string {
  if (buffer && !buffer.endsWith(" ") && chunk && !chunk.startsWith(" ")) {
    return buffer + " " + chunk;
  }
  return buffer + chunk;
}

/**
 * Finalizes the stream buffer by detecting and removing the termination marker "[DONE]".
 *
 * This function checks if the buffer exactly matches or contains the "[DONE]" marker.
 * If the marker is found, it is removed and any extra whitespace is collapsed.
 * The function returns an object containing the cleaned buffer and a boolean flag indicating
 * that the stream has finished.
 *
 * @param {string} buffer - The accumulated text from the stream.
 * @returns {{ buffer: string; done: boolean }} An object with the cleaned buffer and a done flag.
 */
export function finalizeStreamBuffer(buffer: string): {
  buffer: string;
  done: boolean;
} {
  if (buffer === "[DONE]") {
    return { buffer: "", done: true };
  } else if (buffer.includes("[DONE]")) {
    const finalizedBuffer = buffer
      .replace("[DONE]", "")
      .trim()
      .split(/\s+/)
      .join(" ");
    return { buffer: finalizedBuffer, done: true };
  }
  return { buffer, done: false };
}
