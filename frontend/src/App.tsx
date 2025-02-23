/**
 * @file App.tsx - Main entry point for the chat application.
 *
 * This component:
 * - Manages chat interactions via the `useChat` hook.
 * - Displays the conversation (`ChatWindow`).
 * - Allows users to input messages via `ChatInput`.
 * - Handles prompt suggestions for quick replies.
 * - Connects the UI to the FastAPI backend at `/api/chat` via `chatOptions`.
 */

import React, { useState, useMemo } from "react";
import { useChat, type Message } from "@ai-sdk/react";

import { Header } from "@components/ui/header";

import { ChatWindow } from "@components/ui/chat/chat-window";
import { PromptSuggestions } from "@components/ui/chat/prompt-suggestions";
import { ChatInput } from "@components/ui/chat/chat-input";
import { StatusBar } from "@components/status-bar";
import { prompts } from "@data/constants/prompts";

import { chatOptions } from "./config/chat-options";

import { nonBlockingLog } from "@utils/logger";

/**
 * The main chat application component.
 *
 * - Uses `useChat` to manage messages, input state, and API interactions.
 * - Displays chat messages, prompt suggestions, and input field.
 * - Handles UI logic for error states and real-time updates.
 *
 * @component
 * @returns {JSX.Element} The chat application UI.
 */

export default function App() {
  /**
   * Stores any error messages that occur during chat interactions.
   * Used to display error feedback to users.
   *
   * @type {[string | null, React.Dispatch<React.SetStateAction<string | null>>]}
   */
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  /**
   * Controls the visibility of the prompt suggestions panel.
   *
   * When the assistant is actively responding, this panel is hidden.
   *
   * @type {[boolean, React.Dispatch<React.SetStateAction<boolean>>]}
   */
  const [showSuggestions, setShowSuggestions] = useState<boolean>(true);

  /**
   * Memoizes the `chatOptions` configuration to prevent unnecessary re-renders.
   * Ensures that `useChat` does not reinitialize on every render.
   */
  const options = useMemo(
    () => ({
      ...chatOptions,
    }),
    []
  );
  /**
   * Initializes `useChat` to manage chat state and interactions.
   * Connects to the `/api/chat` endpoint.
   * Manages real-time streaming of LLM responses.
   * Handles input changes and message submissions.
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
   * Handles the event when a user selects a prompt suggestion.
   *
   * - Sends the selected prompt to the assistant.
   * - Directly appends the user message without using `handleSubmit`.
   * - Clears the input field after sending.
   *
   * @param {string} promptContent - The selected prompt text.
   * @returns {Promise<void>}
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

    try {
      await append(messagePayload);
      setInput("");
    } catch (error) {
      setErrorMessage("Failed to send prompt. Please try again.");
      nonBlockingLog("🔴 Error sending user prompt:", error);
    }
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
