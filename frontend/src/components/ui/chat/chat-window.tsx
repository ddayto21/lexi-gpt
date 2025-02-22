import React from "react";

import { ChatMessageComponent } from "@components/ui/chat/chat-message";
import type { ChatMessage } from "@components/ui/chat/chat-message";

interface ChatWindowProps {
  messages: ChatMessage[];
  status: string;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ messages, status }) => {
  const filteredMessages = messages.filter((msg) => msg.role !== "system");

  return (
    <main className="flex-1 overflow-auto p-4 space-y-4 bg-black">
      {filteredMessages.map((msg, i) => (
        <ChatMessageComponent key={i} msg={msg} />
      ))}
      {status === "submitted" && (
        <div className="flex items-start justify-start">
          <div className="mr-2 flex-none">
            <div className="h-8 w-8 flex items-center justify-center bg-neutral-800 rounded-full text-sm font-bold">
              AI
            </div>
          </div>
          <div className="max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl px-4 py-3 rounded-2xl shadow bg-neutral-800 rounded-bl-none">
            <div className="text-sm leading-snug whitespace-pre-wrap animate-pulse text-gray-100">
              Assistant is thinking...
            </div>
          </div>
        </div>
      )}
    </main>
  );
};
