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
      className="relative p-2 bg-black border-t border-neutral-800 overflow-hidden"
      style={{
        height: "3rem", // Fixed height to match the screenshot's navigation bar
        backdropFilter: "blur(10px)", // Subtle blur effect like in the screenshot
      }}
    >
      <div className="flex items-center justify-around w-full h-full">
        {/* Render each prompt as a button in a horizontal layout */}
        {filteredPrompts.map((prompt, index) => (
          <button
            key={index}
            onClick={() => handlePromptClick(prompt.content)}
            className="flex items-center justify-center bg-neutral-800 text-gray-100 rounded-full px-4 py-2 text-sm font-medium border border-neutral-700 transition-colors hover:bg-neutral-700 shadow-md duration-300"
            style={{
              minWidth: "120px", // Ensure buttons are evenly spaced and sized
              height: "2.5rem", // Match the button height in the screenshot
            }}
          >
            {prompt.icon && (
              <span className="mr-2 text-lg" role="img" aria-hidden>
                {prompt.icon}
              </span>
            )}
            {prompt.title}
          </button>
        ))}
      </div>
    </aside>
  );
};