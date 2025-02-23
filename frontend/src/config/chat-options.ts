// src/config/chatOptions.ts
import { type UseChatOptions, type Message } from "@ai-sdk/react";
import { nonBlockingLog } from "@utils/logger";

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
  api: "/api/chat",
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
      content: "Hello! I’m here to help you find your next great read.",
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
    nonBlockingLog("fetch() request", url);
    nonBlockingLog("Headers", JSON.stringify(options!.headers, null, 2));
    nonBlockingLog(
      `Body ${JSON.stringify(JSON.parse(options!.body! as string), null, 2)}`
    );
    return await fetch(url, options);
  },
  /**
   * Handles completion of a chat response from the FastAPI server.
   *
   * - This function is triggered **when the assistant finishes responding**.
   * - Logs the completed message for debugging.
   *
   * @param {Message} message - The completed chat message from FastAPI.
   */
  onFinish: (message) => {
    nonBlockingLog("onFinish():");
    nonBlockingLog("🟢 Message sent:", message);
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
    nonBlockingLog("❌ Chat interaction error:", error);
  },

  /**
   * Handles responses received from the FastAPI backend.
   *
   * - Logs the API response for debugging.
   * - Can be extended to trigger UI updates when a response is received.
   *
   * @param {Response} response - The HTTP response object from the FastAPI server.
   */
  onResponse: (response) => {
    nonBlockingLog("📦 Chat response:", response);
  },
};
