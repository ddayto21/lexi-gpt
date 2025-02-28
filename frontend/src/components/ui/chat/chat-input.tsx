/**
 * @file chat-input.tsx - Chat input field and send button component.
 *
 * This component:
 * - Renders an input field and a send button.
 * - Handles user input and submission via form or Enter key.
 * - Updates UI based on chat status and loading state.
 */

import React from "react";
import { SendIcon } from "@components/icons/send-icon";
import { PauseIcon } from "@components/icons/pause-icon";

interface ChatInputProps {
  input: string;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSend: (e: React.FormEvent<HTMLFormElement>) => void;
  status: string; // "ready" | "submitted" | "error"
}

/**
 * Memoized chat input component with form submission handling.
 */
export const ChatInput = React.memo(
  ({ input, onInputChange, onSend, status }: ChatInputProps) => {
    ChatInput.displayName = "ChatInput";

    const isSending = status === "submitted" || status === "streaming";
    const hasInput = input.trim() !== "";
    const isDisabled = status !== "ready";

    // Handle Enter key press to submit the form
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter" && !isDisabled && hasInput) {
        e.preventDefault();
        const formEvent = new Event("submit", {
          bubbles: true,
        }) as unknown as React.FormEvent<HTMLFormElement>;
        onSend(formEvent); // Simulate form submit
      }
    };

    return (
      <footer className="flex items-center p-4 bg-black border-t border-gray-800">
        <input
          className="
        flex-1
        px-4 py-2
        rounded-full
        bg-gray-800 text-gray-100
        placeholder-gray-500
        border border-gray-700
        focus:outline-none
        mr-2
        transition-colors duration-300
      "
          placeholder="Type a message..."
          value={input}
          onChange={onInputChange}
          onKeyDown={handleKeyDown}
          disabled={isDisabled}
        />
        {hasInput && (
          <button
            type="submit"
            disabled={isDisabled}
            className={`
          flex items-center justify-center
          w-10 h-10
          rounded-full
          transition-colors duration-300
          ${
            isDisabled
              ? "bg-gray-700 text-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700 text-white"
          }
        `}
          >
            {isSending ? <PauseIcon /> : <SendIcon />}
          </button>
        )}
      </footer>
    );
  }
);
