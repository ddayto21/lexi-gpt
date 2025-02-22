import React, { useState } from "react";
import { useChat, type Message, type UseChatOptions } from "@ai-sdk/react";
import { parseSseData } from "@utils/parse-sse-data";

import { Header } from "@components/ui/header";

import { ChatWindow } from "@components/ui/chat/chat-window";
import { PromptSuggestions } from "@components/ui/chat/prompt-suggestions";
import { ChatInput } from "@components/ui/chat/chat-input";
import { StatusBar } from "@components/status-bar";
import { prompts } from "@data/constants/prompts";

export interface ChatMessage extends Message {
  timestamp?: string;
}

export default function App() {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showSuggestions, setShowSuggestions] = useState(true);

  /**
   * @description Configuration for the useChat hook, defining the interaction with the backend API.
   * This object sets up the connection to the chat completion endpoint, specifies the streaming protocol,
   * provides initial chat messages, and defines callback functions for handling responses, errors, and the completion of a message.
   */
  const options: UseChatOptions = {
    /**
     * @description The API endpoint for chat completions. This URL is proxied by the frontend
     * to the backend's `/chat` route, which in turn forwards requests to the DeepSeek LLM API.
     * @type {string}
     */
    api: "/api/chat",

    streamProtocol: "text",

    /**
     * @description Initial messages displayed in the chat window. This provides a starting point for the conversation.
     * @type {ChatMessage[]}
     */
    initialMessages: [
      {
        id: "1",
        role: "assistant",
        content:
          "Hello! I am a book recommendation assistant.  To give you the best recommendations, please tell me what you're looking for in a book.  For example, you can tell me the genre, themes, authors you like, or anything else that's important to you.",
        timestamp: new Date().toISOString(),
      } as ChatMessage,
    ],

    /**
     * @description Flag to enable or disable sending extra message fields in the request to the chat API.
     * If this is not set to true, then the message content is the only field sent to the API.
     * @type {boolean}
     */
    sendExtraMessageFields: true,
    /**
     * @description Callback function called when a complete message has been received and processed.
     * The `message` object contains the full content of the streamed response, which might need parsing.
     * @param {ChatMessage} message The completed chat message.
     */

    onFinish: (message) => {
      console.log("Raw message content:", message.content);
      const formattedMessage = parseSseData(message.content);
      console.log("Finished streaming message:", formattedMessage);
      setShowSuggestions(true);
    },
    /**
     * @description Callback function called when an error occurs during the chat interaction.
     * @param {Error} error The error object.
     */
    onError: (error) => {
      console.error("An error occurred:", error);
      setErrorMessage(error.message || "An unknown error occurred.");
    },
    /**
     * @description Callback function called when an HTTP response is received from the server.
     * This can be used for logging or other processing of the response.
     * @param {Response} response The HTTP response object.
     */
    onResponse: (response) => {
      console.log("Received HTTP response from server:", response);
      const headers = response.headers;
      console.log("Response headers:", headers);
    },
  };

  const { messages, input, status, handleInputChange, append } =
    useChat(options);

  async function sendMessage() {
    console.log(`sendMessage() `)
    await sendMessageWithContent(input);
  }

  // New: Generalized send function that clears the input immediately
  async function sendMessageWithContent(content: string) {
    console.log(`sendMessageWithContent(content) `)
    console.log(`content: ${content} `)
    if (!content.trim()) return; // What does !content.trim() mean?

    const messagePayload: ChatMessage = {
      id: String(Date.now()),
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    };

    console.debug("Sending message payload to /api/chat: (messagePayload):");
    console.log(messagePayload);

    await append(messagePayload);
  }

  // When a prompt is clicked, that message and hide suggestions.
  const onPromptClick = (promptContent: string) => {
    console.log(`onPromptClick() `)
    sendMessageWithContent(promptContent);
    setShowSuggestions(false);
  };

  return (
    <div className="flex flex-col h-screen bg-black text-white font-sans">
      <Header />

      <StatusBar status={status} errorMessage={errorMessage} />

      {/* Chat messages container */}
      <ChatWindow messages={messages as ChatMessage[]} status={status} />

      {showSuggestions && (
        <PromptSuggestions
          examplePrompts={prompts}
          onPromptClick={onPromptClick}
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
