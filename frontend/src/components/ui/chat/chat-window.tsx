import React, { useRef, useEffect } from "react";
import { ChatMessageComponent } from "@components/ui/chat/chat-message";
import { Message } from "@ai-sdk/ui-utils";
import { Loading } from "@components/ui/loading";

interface ChatWindowProps {
  messages: Message[];
  status: string;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ messages, status }) => {
  const filteredMessages = messages.filter(
    (msg) => msg.role === "user" || msg.role === "assistant"
  );
  const lastMessageRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (status === "submitted" && lastMessageRef.current) {
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
                  <span className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0s" }}></span>
                  <span className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></span>
                  <span className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0.4s" }}></span>
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
};