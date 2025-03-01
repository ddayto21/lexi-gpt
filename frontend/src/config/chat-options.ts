// src/config/chatOptions.ts
import { type UseChatOptions, type Message } from "@ai-sdk/react";

if (!process.env.REACT_APP_BASE_URL) {
  throw new Error("REACT_APP_BASE_URL is not set");
}

const BASE_API_URL = process.env.REACT_APP_BASE_URL;

/**
 * @description Configuration for the useChat hook, defining the interaction with the backend API.
 * This object sets up the connection to the chat completion endpoint, specifies the streaming protocol,
 * provides initial chat messages, and defines callback functions for handling responses, errors, and the completion of a message.
 */

export const chatOptions: UseChatOptions = {
  /**
   * The API endpoint that the chat system communicates with.
   *
   * This endpoint (`/api/chat`) is handled by the FastAPI server, which:
   * - Receives user messages.
   * - Streams AI-generated responses back to the client using Server-Sent Events (SSE).
   * - Supports real-time updates, enabling smooth conversation flow.
   *
   * @type {string}
   */
  api: `${BASE_API_URL}/chat`,
  /**
   * Specifies the protocol used to stream AI-generated responses.
   *
   * The `"text"` protocol ensures that the response is streamed **incrementally**,
   * allowing real-time UI updates in React as messages arrive from FastAPI.
   *
   * @type {string}
   */
  streamProtocol: "text",
  /**
   * Initial system message that appears when the chat starts.
   *
   * This predefined message:
   * - Welcomes the user.
   * - Guides them on how to interact with the assistant.
   * - Ensures a conversational starting point before the first user input.
   *
   * @type {Message[]}
   */
  initialMessages: [
    {
      id: "1",
      role: "assistant",
      content:
        "Hey there! 👋 I'm LexiGPT, your friendly librarian. Tell me what you're in the mood for—thrillers, romance, or a hidden gem—and I'll find your next great read! 😊",
      timestamp: new Date().toISOString(),
    } as Message,
  ],
  /**
   * Determines whether additional message fields should be included in requests.
   *
   * Setting this to `true` ensures that extra metadata (such as timestamps)
   * is sent along with the user message to the FastAPI backend.
   *
   * @type {boolean}
   */
  sendExtraMessageFields: true,
  /**
   * Custom fetch implementation that logs outgoing API requests.
   *
   * This function:
   * - Intercepts requests sent to `/api/chat`.
   * - Logs the request URL, headers, and body for debugging.
   * - Forwards the request to the FastAPI backend.
   *
   * @param {string} url - The API endpoint URL.
   * @param {RequestInit} options - Fetch request options (headers, method, body).
   * @returns {Promise<Response>} - The API response from FastAPI.
   */
  fetch: async (url, options) => {
    return await fetch(url, {
      ...options,
      credentials: "include",
    });
  },

  /**
   * Handles errors encountered during the chat interaction.
   *
   * - If an error occurs (e.g., network failure, invalid response), it is logged.
   * - This prevents UI crashes and helps with debugging API issues.
   *
   * @param {Error} error - The error object representing the issue.
   */
  onError: (error) => {
    console.error("❌ Chat interaction error:", error);
  },

  /**
   * Handles responses received from the FastAPI backend.
   *
   * - Logs the API response for debugging.
   * - Can be extended to trigger UI updates when a response is received.
   *
   * @param {Response} response - The HTTP response object from the FastAPI server.
   */
  // onResponse: (response) => {
  //   console.log("📦 Chat response:", response);
  // },
};
