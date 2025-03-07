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
        onSend(
          new Event("submit", {
            bubbles: true,
          }) as unknown as React.FormEvent<HTMLFormElement>
        );
      }
    };

    return (
      <footer className="flex items-center p-4 bg-black border-t border-gray-900">
        <form onSubmit={onSend} className="flex items-center w-full max-w-3xl mx-auto">
          <input
            className="
           flex-1
            px-5 py-3
            rounded-full
            bg-gray-900 text-gray-100
            placeholder-gray-500
            border border-gray-800
            focus:outline-none focus:ring-2 focus:ring-blue-500/50
            transition-all duration-300
            "
            placeholder="How can I help?"
            value={input}
            onChange={onInputChange}
            onKeyDown={handleKeyDown}
            disabled={isDisabled}
            aria-label="Chat input"
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
                    ? "bg-gray-800 text-gray-500 cursor-not-allowed"
                    : "bg-gradient-to-br from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg shadow-blue-500/30"
                }
              `}
            >
              {isSending ? <PauseIcon /> : <SendIcon />}
            </button>
          )}
        </form>
      </footer>
    );
  }
);
