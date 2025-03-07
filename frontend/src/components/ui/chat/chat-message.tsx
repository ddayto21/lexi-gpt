import React, { useMemo, forwardRef } from "react";
import type { Message } from "@ai-sdk/react";
import { AiAvatar } from "../avatars/ai-avatar";
import { formatContent, getTimeAgo } from "../../../utils/parse-sse-data";
import { ChatMarkdown } from "./chat-markdown";

export interface ChatMessage extends Message {
  timestamp?: string;
}

interface ChatMessageProps {
  msg: ChatMessage;
}

export const ChatMessageComponent = forwardRef<
  HTMLDivElement,
  ChatMessageProps
>(({ msg }, ref) => {
  const isAssistant = msg.role === "assistant";
  const content = useMemo(() => {
    try {
      return formatContent(msg);
    } catch (error) {
      console.error("Error parsing message content", error);
      return "An error occurred while parsing the message content.";
    }
  }, [msg]);
  const relativeTime = msg.timestamp ? getTimeAgo(msg.timestamp) : "";

  return (
    <div
      ref={ref}
      className={`flex items-start ${
        isAssistant ? "justify-start" : "justify-end"
      } animate-fade-in`}
    >
      {isAssistant && (
        <div className="mr-3 flex-none">
          <AiAvatar />
        </div>
      )}
      <div
        className={`
          max-w-xs sm:max-w-md md:max-w-lg lg:max-w-2xl
          px-4 py-3 rounded-2xl shadow-md
          transition-all duration-200 hover:shadow-lg
          ${
            isAssistant
              ? "bg-gray-800 text-gray-200 rounded-bl-none"
              : "bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-br-none"
          }
        `}
      >
        <div className="flex items-center gap-2 mb-1">
          <span className="font-medium text-sm">
            {isAssistant ? "LexiGPT" : "You"}
          </span>
          {relativeTime && (
            <span className="text-xs text-gray-400">{relativeTime}</span>
          )}
        </div>
        <div className="text-sm leading-relaxed whitespace-pre-wrap">
          <ChatMarkdown content={content} />
        </div>
      </div>
      {!isAssistant && (
        <div className="ml-3 flex-none">
          <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-600 to-purple-700 shadow-md" />
        </div>
      )}
    </div>
  );
});
ChatMessageComponent.displayName = "ChatMessageComponent";
