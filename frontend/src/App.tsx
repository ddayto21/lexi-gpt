import React, { useState, useMemo } from "react";
import { useChat, type Message, type UseChatOptions } from "@ai-sdk/react";

import { Header } from "@components/ui/header";

import { ChatWindow } from "@components/ui/chat/chat-window";
import { PromptSuggestions } from "@components/ui/chat/prompt-suggestions";
import { ChatInput } from "@components/ui/chat/chat-input";
import { StatusBar } from "@components/status-bar";
import { prompts } from "@data/constants/prompts";

import { chatOptions } from "./config/chat-options";

import { nonBlockingLog } from "@utils/logger";

export default function App() {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(true);
  nonBlockingLog("🟢 `useChat` initialized in `App.tsx`");

  console.log("🟢 `useChat` initialized in `App.tsx`");

  /**
   * ✅ Memoize `options` to prevent `useChat` from reinitializing on every render.
   */
  const options = useMemo(() => chatOptions, []); // ✅ Memoize imported options

  /**
   * ✅ Use `useChat` with memoized options
   */
  const {
    messages,
    input,
    status,
    append,
    setInput,
    handleInputChange,
    handleSubmit,
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

      <ChatInput
        input={input}
        onInputChange={handleInputChange}
        onSend={handleSubmit}
        status={status}
      />
    </div>
  );
}
