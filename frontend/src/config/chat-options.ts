// src/config/chatOptions.ts
import { type UseChatOptions, type Message } from "@ai-sdk/react";
import { nonBlockingLog } from "@utils/logger";

/**
 * @description Configuration for the useChat hook, defining the interaction with the backend API.
 * This object sets up the connection to the chat completion endpoint, specifies the streaming protocol,
 * provides initial chat messages, and defines callback functions for handling responses, errors, and the completion of a message.
 */

export const chatOptions: UseChatOptions = {
  api: "/api/chat",
  streamProtocol: "text",
  initialMessages: [
    {
      id: "1",
      role: "assistant",
      content: "Hello! I’m here to help you find your next great read.",
      timestamp: new Date().toISOString(),
    } as Message,
  ],
  sendExtraMessageFields: true,

  fetch: async (url, options) => {
    nonBlockingLog("fetch() request", url);
    nonBlockingLog("Headers", JSON.stringify(options!.headers, null, 2));
    nonBlockingLog(
      `Body ${JSON.stringify(JSON.parse(options!.body! as string), null, 2)}`
    );
    return await fetch(url, options);
  },

  onFinish: (message) => {
    nonBlockingLog("onFinish():");
    nonBlockingLog("🟢 Message sent:", message);
  },

  onError: (error) => {
    nonBlockingLog("❌ Chat interaction error:", error);
  },

  onResponse: (response) => {
    nonBlockingLog("📦 Chat response:", response);
  },
};
