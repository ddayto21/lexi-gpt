// App.tsx
import React, { useState } from "react";
import { useChat, type UseChatOptions, type Message } from "@ai-sdk/react";
import { parseSseData } from "@utils/parse-sse-data";

export function formatContent(message: Message): string {
  if (
    message.role === "assistant" &&
    message.content.trim().startsWith("data:")
  ) {
    return parseSseData(message.content);
  }
  return message.content;
}

export default function App() {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const options: UseChatOptions = {
    api: "/api/completion",
    streamProtocol: "text",
    initialMessages: [
      {
        id: "1",
        role: "assistant",
        content:
          "Hello! I can help you find a book. Please describe your interests.",
      },
    ],
    onFinish: (message) => {
      // Parse the raw SSE data before printing/logging.
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

  const { messages, input, status, handleInputChange, handleSubmit } =
    useChat(options);

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="flex items-center justify-between px-4 py-2 bg-gray-900 text-white"></div>
      {/* Status/Error messages */}
      <div className="p-4">
        <p>Status: {status}</p>
        {errorMessage && (
          <div className="mt-2 p-2 bg-red-500 text-white rounded">
            Error: {errorMessage}
          </div>
        )}
      </div>

      {/* Chat messages */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((msg, i) => {
          const content = formatContent(msg);
          return (
            <div
              key={i}
              className={`max-w-xl ${
                msg.role === "assistant"
                  ? "self-start bg-white text-black rounded p-3"
                  : "self-end bg-blue-500 text-white rounded p-3"
              }`}
            >
              <div> {msg.role === "assistant" ? "Assistant" : "You"} </div>
              <div> {content} </div>
            </div>
          );
        })}
      </div>

      {/* Input area */}
      <div className="flex items-center gap-2 p-4 bg-gray-200 border-t border-gray-300">
        <input
          className="flex-1 px-3 py-2 rounded border border-gray-400"
          placeholder="Describe a book you are looking for..."
          value={input}
          onChange={handleInputChange}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
        />
        <button
          onClick={handleSubmit}
          disabled={status === "submitted" || input === ""}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
