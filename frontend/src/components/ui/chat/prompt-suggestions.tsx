import React, { useState } from "react";

interface PromptSuggestion {
  title: string;
  description?: string;
  content: string;
  icon?: string;
}

interface PromptSuggestionsProps {
  examplePrompts: PromptSuggestion[];
  onPromptClick: (prompt: string) => void;
}

export const PromptSuggestions: React.FC<PromptSuggestionsProps> = ({
  examplePrompts,
  onPromptClick,
}) => {
  // Tracks whether the suggestions are collapsed or expanded
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Toggle collapse state
  function toggleCollapse() {
    setIsCollapsed((prev) => !prev);
  }

  return (
    <aside
      className="
        relative
        p-3
        bg-black/60
        backdrop-blur-sm
        transition-all
        duration-300
      "
      // If collapsed, reduce height drastically, hide overflow
      style={{
        maxHeight: isCollapsed ? "2rem" : "40%",
        overflowY: isCollapsed ? "hidden" : "auto",
      }}
    >
      <div className="flex items-center justify-between">
        <p className="text-base font-semibold text-gray-200">
          {isCollapsed ? "" : "Select a topic"}
        </p>
        <button
          onClick={toggleCollapse}
          className="
            text-gray-400
            hover:text-gray-200
            text-sm
            transition-colors
            bg-neutral-800/50
            rounded-full
            px-2 py-1
          "
          aria-label="Toggle suggestions"
        >
          {isCollapsed ? "▲" : "▼"}
        </button>
      </div>

     
     
      {!isCollapsed && (
        <div
          className="
            flex flex-wrap
            gap-2

            overflow-x-auto scrollbar-custom
            whitespace-nowrap
            h-full
          "
        >
          {examplePrompts.map((prompt, index) => (
            <button
              key={index}
              onClick={() => onPromptClick(prompt.content)}
              className="
                inline-flex items-center 
                bg-neutral-800 text-gray-100
                rounded-full px-4 py-2
                text-sm font-medium
                border border-neutral-700
                transition-colors 
                hover:bg-neutral-700
                whitespace-nowrap
              "
            >
              {prompt.icon && (
                <span className="mr-2" role="img" aria-hidden>
                  {prompt.icon}
                </span>
              )}
              {prompt.title}
            </button>
          ))}
        </div>
      )}
    </aside>
  );
};
