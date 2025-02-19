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

  const { messages, input, status, setInput, handleInputChange, handleSubmit } =
    useChat(options);

  // Quick reply suggestions for users
  const quickReplies = [
    "I'm into mystery novels",
    "I love sci-fi adventures",
    "Recommend a classic literature",
    "Show me some thrillers",
  ];

   // When a quick reply is clicked, update the hook's input.
   const onQuickReplyClick = (reply: string) => {
    setInput(reply);
  };

  return (
    <div className="flex flex-col h-screen bg-black text-white font-sans">
      <div className="flex items-center justify-center py-3 bg-gray-900 border-b border-gray-700">
        <h1 className="text-lg font-bold">AI Book Finder</h1>
      </div>

      {/* Status/Error messages */}
      <div className="px-4 py-2 border-b border-gray-700">
        {" "}
        <p className="text-sm">Status: {status}</p>
        {errorMessage && (
          <div className="mt-2 p-2 bg-red-600 text-white rounded-md">
            Error: {errorMessage}
          </div>
        )}
      </div>
      {/* Chat messages */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((msg, i) => {
          const content = formatContent(msg);
          const isAssistant = msg.role === "assistant";

          return (
            <div
              key={i}
              className={`flex items-start ${
                isAssistant ? "justify-start" : "justify-end"
              }`}
            >
              {/* Avatar */}
              {isAssistant ? (
                <div className="mr-2 flex-none">
                  {/* Replace this with an AI logo or image */}
                  <div className="h-8 w-8 flex items-center justify-center bg-gray-700 rounded-full text-sm font-bold">
                    AI
                  </div>
                </div>
              ) : (
                <div className="mr-2 flex-none">
                  {/* Gradient avatar for user */}
                  <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-600 to-purple-600" />
                </div>
              )}

              {/* Message bubble */}
              <div
                className={`max-w-xs md:max-w-md px-4 py-3 rounded-2xl shadow ${
                  isAssistant
                    ? "bg-gray-800 rounded-bl-none"
                    : "bg-blue-600 rounded-br-none"
                }`}
              >
                <div className="text-sm leading-snug whitespace-pre-wrap">
                  {content}
                </div>
              </div>
            </div>
          );
        })}

        {/* Typing indicator when AI is streaming */}
        {status === "submitted" && (
          <div className="flex items-start justify-start">
            <div className="mr-2 flex-none">
              <div className="h-8 w-8 flex items-center justify-center bg-gray-700 rounded-full text-sm font-bold">
                AI
              </div>
            </div>
            <div className="max-w-xs md:max-w-md px-4 py-3 rounded-2xl shadow bg-gray-800 rounded-bl-none">
              <div className="text-sm leading-snug whitespace-pre-wrap animate-pulse">
                Assistant is typing...
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Quick-Reply Suggestions */}
      <div className="px-4 py-2 border-t border-gray-700">
        <p className="mb-2 text-sm">Quick Suggestions:</p>
        <div className="flex gap-2 flex-wrap">
          {quickReplies.map((reply, index) => (
            <button
              key={index}
              onClick={() => onQuickReplyClick(reply)}
              className="px-3 py-1 bg-gray-700 text-white rounded-full text-sm hover:bg-gray-600"
            >
              {reply}
            </button>
          ))}
        </div>
      </div>

      {/* Input area */}
      <div className="flex items-center p-4 bg-gray-900 border-t border-gray-700">
        <input
          className="flex-1 px-4 py-2 rounded-full bg-gray-800 text-white placeholder-gray-400 border border-gray-700 focus:outline-none mr-2"
          placeholder="Describe a book you are looking for..."
          value={input}
          onChange={handleInputChange}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
        />
        <button
          onClick={handleSubmit}
          disabled={status === "submitted" || input === ""}
          className="px-5 py-2 bg-blue-600 text-white rounded-full disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
