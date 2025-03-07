import React, { useRef, useEffect } from "react";
import { ChatMessageComponent } from "@components/ui/chat/chat-message";
import { Message } from "@ai-sdk/ui-utils";

/**
 * Props for the ChatWindow component.
 * @typedef {Object} ChatWindowProps
 * @property {Message[]} messages - Array of chat messages to display.
 * @property {string} status - Current status of the chat (e.g., "ready", "submitted", "streaming").
 */
interface ChatWindowProps {
  messages: Message[];
  status: string;
}

/**
 * Displays the chat conversation and handles scrolling behavior.
 *
 * This component renders a list of messages and ensures the view scrolls to the latest message
 * when the assistant is streaming a response or has just submitted one. It uses a ref to track
 * the last message and triggers smooth scrolling when the status indicates activity.
 *
 * @component
 * @param {ChatWindowProps} props - The properties passed to the component.
 * @returns {JSX.Element} The rendered chat window.
 */
export const ChatWindow: React.FC<ChatWindowProps> = ({ messages, status }) => {
  // Filter messages to only show user and assistant roles
  const filteredMessages = messages.filter(
    (msg) => msg.role === "user" || msg.role === "assistant"
  );

  // Ref to track the latest message or streaming indicator
  const lastMessageRef = useRef<HTMLDivElement | null>(null);

  /**
   * Scrolls to the bottom of the chat when the assistant is streaming or has submitted a response.
   *
   * This effect runs whenever the `status` or `filteredMessages` changes. It checks if the status
   * is "streaming" (assistant response in progress) or "submitted" (response just started), and
   * if a ref to the last message exists, it smoothly scrolls to that element. This ensures the
   * user always sees the latest content as it arrives.
   */
  useEffect(() => {
    if (
      (status === "submitted" || status === "streaming") &&
      lastMessageRef.current
    ) {
      lastMessageRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [status, filteredMessages]);

  return (
    <main className="flex-1 overflow-auto p-6 bg-black flex justify-center">
      <div className="w-full max-w-3xl space-y-3">
        {filteredMessages.map((message, index) => (
          <ChatMessageComponent
            key={index}
            msg={message}
            ref={index === filteredMessages.length - 1 ? lastMessageRef : null}
          />
        ))}
        {status === "submitted" && (
          <div className="flex items-start animate-fade-in-custom">
            <div className="mr-3 flex-none">
              <div className="h-8 w-8 flex items-center justify-center bg-gray-800 rounded-full text-sm font-medium text-gray-300">
                AI
              </div>
            </div>
            <div className="px-4 py-2 rounded-xl bg-gray-900 text-gray-300">
              <div className="flex items-center space-x-2">
                <span className="text-sm animate-pulse">Thinking</span>
                <span className="flex space-x-1">
                  <span
                    className="w-1 h-1 bg-blue-500 rounded-full animate-bounce"
                    style={{ animationDelay: "0s" }}
                  ></span>
                  <span
                    className="w-1 h-1 bg-blue-500 rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></span>
                  <span
                    className="w-1 h-1 bg-blue-500 rounded-full animate-bounce"
                    style={{ animationDelay: "0.4s" }}
                  ></span>
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
};
