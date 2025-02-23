import React, { useState, useMemo } from "react";
import { useChat, type Message, type UseChatOptions } from "@ai-sdk/react";

import { Header } from "@components/ui/header";

import { ChatWindow } from "@components/ui/chat/chat-window";
import { PromptSuggestions } from "@components/ui/chat/prompt-suggestions";
import { ChatInput } from "@components/ui/chat/chat-input";
import { StatusBar } from "@components/status-bar";
import { prompts } from "@data/constants/prompts";
import { nonBlockingLog } from "@utils/logger";

export default function App() {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showSuggestions, setShowSuggestions] = useState(true);

  nonBlockingLog("🟢 `useChat` initialized in `App.tsx`");

  /**
   * @description Configuration for the useChat hook, defining the interaction with the backend API.
   * This object sets up the connection to the chat completion endpoint, specifies the streaming protocol,
   * provides initial chat messages, and defines callback functions for handling responses, errors, and the completion of a message.
   */

  /**
   * ✅ Memoize `options` to prevent `useChat` from reinitializing on every render.
   */
  const options: UseChatOptions = useMemo(
    () => ({
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
          `Body ${JSON.stringify(
            JSON.parse(options!.body! as string),
            null,
            2
          )}`
        );
        return await fetch(url, options);
      },
      onFinish: (message) => {
        nonBlockingLog("onFinish():");
        nonBlockingLog("🟢 Message sent:", message);
        setShowSuggestions(true);
      },

      onError: (error) => {
        nonBlockingLog("❌ Chat interaction error:", error);
        setErrorMessage(error.message || "An unknown error occurred.");
      },

      onResponse: (response) => {
        nonBlockingLog("📦 Chat response:", response);
        setShowSuggestions(false);
      },
    }),

    []
  ); // ✅ Empty dependency array ensures this only initializes once.

  const {
    messages,

    status,

    append,

    setInput, // ✅ Directly update the input state
  } = useChat(options);

  /**
   * Handles prompt suggestions being clicked.
   */
  const onPromptClick = async (promptContent: string) => {
    if (!promptContent.trim()) return;

    nonBlockingLog(`🟠 onPromptClick() → Sending prompt: "${promptContent}"`);

    const messagePayload: Message = {
      id: String(Date.now()),
      role: "user",
      content: promptContent,
      createdAt: new Date(),
    };

    nonBlockingLog("📦 Sending user prompt:", messagePayload);

    await append(messagePayload); // ✅ Directly appends without using `handleSubmit`
    setInput(""); // ✅ Clears input after sending
  };

  return (
    <div className="flex flex-col h-screen bg-black text-white font-sans">
      <Header />

      <StatusBar status={status} errorMessage={errorMessage} />

      <ChatWindow messages={messages as Message[]} status={status} />

      {showSuggestions && (
        <PromptSuggestions
          examplePrompts={prompts}
          onPromptClick={onPromptClick}
        />
      )}

      <ChatInput />
    </div>
  );
}
