import React from "react";

export interface QuickReply {
  icon: string;
  title: string;
  content: string;
  description: string;
}

interface PromptSuggestionsProps {
  examplePrompts: QuickReply[];
  onPromptClick: (replyContent: string) => void;
  onClose: () => void;
}

export const PromptSuggestions: React.FC<PromptSuggestionsProps> = ({
  examplePrompts,
  onPromptClick,
  onClose,
}) => (
  <aside className="relative px-4 py-3 border-t border-neutral-800 bg-neutral-900">
    <div className="flex items-center justify-between mb-2">
      <p className="text-sm font-semibold text-gray-200">Topics</p>
      <button
        onClick={onClose}
        className="text-gray-500 hover:text-gray-300 transition-colors"
        aria-label="Close suggestions"
      >
        ✕
      </button>
    </div>
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {examplePrompts.map((reply, index) => (
        <button
          key={index}
          onClick={() => onPromptClick(reply.content)}
          className="flex items-center p-3 border border-neutral-700 bg-[#1a1a1a] hover:bg-[#2a2a2a] text-gray-300 rounded-md transition-colors"
        >
          <div className="mr-3 text-lg">{reply.icon}</div>
          <div className="text-left">
            <div className="text-sm font-semibold text-gray-100">
              {reply.title}
            </div>
            <div className="text-xs text-gray-400">{reply.description}</div>
          </div>
        </button>
      ))}
    </div>
  </aside>
);
