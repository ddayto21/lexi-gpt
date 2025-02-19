import React from "react";
import type { Message } from "@ai-sdk/react";
import { AiAvatar } from "@components/ui/avatars/ai-avatar";
import { formatContent, getTimeAgo } from "@utils/parse-sse-data";
export interface ChatMessage extends Message {
  timestamp?: string;
}

interface ChatMessageProps {
  msg: ChatMessage;
}

export const ChatMessageComponent: React.FC<ChatMessageProps> = ({ msg }) => {
  const isAssistant = msg.role === "assistant";
  let content;

  try {
    content = formatContent(msg);
  } catch (error) {
    console.error("Error parsing message content", error);
    content = "An error occurred while parsing the message content";
  }
  const formattedContent = content.replace(/\n/g, "<br />");

  const relativeTime = msg.timestamp ? getTimeAgo(msg.timestamp) : "";

  return (
    <div
      className={`flex items-start ${
        isAssistant ? "justify-start" : "justify-end"
      }`}
    >
      {/* Avatar */}
      {isAssistant ? (
        <div className="mr-2 flex-none">
          <AiAvatar />
        </div>
      ) : (
        <div className="mr-2 flex-none">
          <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-600 to-purple-600" />
        </div>
      )}

      {/* Message bubble */}
      <div
        className={`max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl px-4 py-3 rounded-2xl shadow ${
          isAssistant
            ? "bg-neutral-800 rounded-bl-none"
            : "bg-blue-600 rounded-br-none"
        }`}
      >
        {/* Header row: name + relative timestamp */}
        <div className="flex items-center gap-2 mb-1">
          <span className="font-semibold text-sm text-gray-200">
            {isAssistant ? "Assistant" : "You"}
          </span>
          {relativeTime && (
            <span className="text-xs text-gray-400">{relativeTime}</span>
          )}
        </div>
        <div className="text-sm leading-snug whitespace-pre-wrap text-gray-100">
          {content}
        </div>
      </div>
    </div>
  );
};
