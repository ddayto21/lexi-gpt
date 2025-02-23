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
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [selectedPrompts, setSelectedPrompts] = useState<Set<string>>(
    new Set()
  );

  function toggleCollapse() {
    setIsCollapsed((prev) => !prev);
  }

  const handlePromptClick = (promptContent: string) => {
    if (!selectedPrompts.has(promptContent)) {
      setSelectedPrompts((prev) => {
        const newSelectedPrompts = new Set(prev);
        newSelectedPrompts.add(promptContent);
        return newSelectedPrompts;
      });
      onPromptClick(promptContent);
      setIsCollapsed(true); // Collapse the menu after selecting a prompt
    }
  };

  const filteredPrompts = examplePrompts.filter(
    (prompt) => !selectedPrompts.has(prompt.content)
  );

  return (
    <aside
      className="relative p-3 bg-black/60 backdrop-blur-sm transition-all duration-300 border-t border-neutral-800 overflow-hidden"
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
          className="text-gray-400 hover:text-gray-200 text-sm transition-colors bg-neutral-800/50 rounded-full px-2 py-1"
          aria-label="Toggle suggestions"
        >
          {isCollapsed ? "▲" : "▼"}
        </button>
      </div>

      {!isCollapsed && (
        <div className="mt-2 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 overflow-y-auto scrollbar-custom">
          {filteredPrompts.map((prompt, index) => (
            <button
              key={index}
              onClick={() => handlePromptClick(prompt.content)}
              className="flex items-center bg-neutral-800 text-gray-100 rounded-full px-4 py-2 text-sm font-medium border border-neutral-700 transition-colors hover:bg-neutral-700 whitespace-nowrap shadow-md duration-300"
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
