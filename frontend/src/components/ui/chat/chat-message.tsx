import React, { useMemo } from "react";
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

export const ChatMessageComponent: React.FC<ChatMessageProps> = ({ msg }) => {
  const isAssistant = msg.role === "assistant";

  const content = useMemo(() => {
    try {
      const formatted = formatContent(msg);
      console.log("after formatting the content:", formatted);
      return formatted;
    } catch (error) {
      console.error("Error parsing message content", error);
      return "An error occurred while parsing the message content.";
    }
  }, [msg]);

  const relativeTime = msg.timestamp ? getTimeAgo(msg.timestamp) : "";

  return (
    <div className={`flex items-start ${isAssistant ? "justify-start" : "justify-end"}`}>
      {isAssistant ? (
        <div className="mr-2 flex-none">
          <AiAvatar />
        </div>
      ) : (
        <div className="mr-2 flex-none">
          <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-600 to-purple-600" />
        </div>
      )}

      <div
        className={`max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl px-4 py-3 rounded-2xl shadow ${
          isAssistant ? "bg-neutral-800 rounded-bl-none" : "bg-blue-600 rounded-br-none"
        }`}
      >
        <div className="flex items-center gap-2 mb-1">
          <span className="font-semibold text-sm text-gray-200">
            {isAssistant ? "LexiGPT" : "You"}
          </span>
          {relativeTime && <span className="text-xs text-gray-400">{relativeTime}</span>}
        </div>

        {/* Use whitespace-pre-wrap so the final HTML respects line breaks,
            but combined with our forced newline logic, each line is truly separate. */}
        <div className="text-sm leading-snug whitespace-pre-wrap text-gray-100">
          <ChatMarkdown content={content} />
        </div>
      </div>
    </div>
  );
};