import React, { useState } from "react";
import { useChat, type Message, type UseChatOptions } from "@ai-sdk/react";
import { parseSseData } from "@utils/parse-sse-data";

import { Header } from "@components/ui/header";

import { ChatWindow } from "@components/ui/chat/chat-window";
import { PromptSuggestions } from "@components/ui/chat/prompt-suggestions";
import { ChatInput } from "@components/ui/chat/chat-input";
import { StatusBar } from "@components/status-bar";
import { prompts } from "@data/constants/prompts";

// 1. Extend the default Message type to include a timestamp.
export interface ChatMessage extends Message {
  timestamp?: string;
}

export default function App() {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showSuggestions, setShowSuggestions] = useState(true);

  const options: UseChatOptions = {
    api: "/api/completion",
    streamProtocol: "text",
    initialMessages: [
      {
        id: "1",
        role: "assistant",
        content:
          "Hello! I am a book recommendation assistant.  To give you the best recommendations, please tell me what you're looking for in a book.  For example, you can tell me the genre, themes, authors you like, or anything else that's important to you.",
        timestamp: new Date().toISOString(),
      } as ChatMessage,
    ],
    onFinish: (message) => {
      const formattedMessage = parseSseData(message.content);
      console.log("Finished streaming message:", formattedMessage);
    },
    onError: (error) => {
      console.error("An error occurred:", error);
      setErrorMessage(error.message || "An unknown error occurred.");
    },
    onResponse: (response) => {
      console.log("Received HTTP response from server:", response);
    },
  };

  const { messages, input, setInput, handleInputChange, append, status } =
    useChat(options);

  async function sendMessage() {
    await sendMessageWithContent(input);
  }

  // New: Generalized send function that clears the input immediately
  async function sendMessageWithContent(content: string) {
    if (!content.trim()) return;
    // Clear the input before sending to immediately give feedback.
    setInput("");
    await append({
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    } as ChatMessage);
  }

  // When a prompt is clicked, auto-send that message and hide suggestions.
  const onPromptClick = (replyContent: string) => {
    sendMessageWithContent(replyContent);
    setShowSuggestions(false);
  };

  return (
    <div className="flex flex-col h-screen bg-black text-white font-sans py-10 px-10">
      <Header />

      <StatusBar status={status} errorMessage={errorMessage} />

      {/* Chat messages container */}
      <ChatWindow messages={messages as ChatMessage[]} status={status} />

      {/* Quick-Reply Suggestions */}
      {showSuggestions && (
        <PromptSuggestions
          examplePrompts={prompts}
          onPromptClick={onPromptClick}
          onClose={() => setShowSuggestions(false)}
        />
      )}

      {/* Input area */}
      <ChatInput
        input={input}
        onInputChange={handleInputChange}
        onSend={sendMessage}
        status={status}
      />
    </div>
  );
}
