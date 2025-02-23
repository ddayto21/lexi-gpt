import React from "react";
import { SendIcon } from "@components/icons/send-icon";
import { PauseIcon } from "@components/icons/pause-icon";

interface ChatInputProps {
  input: string;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSend: () => void;
  status: string; // "ready" | "submitted" | "error" etc.
}

/**
 * `ChatInput` is a memoized React functional component that renders a chat input field and a send button.
 * 
 * @param {Object} props - The properties object.
 * @param {string} props.input - The current value of the input field.
 * @param {function} props.onInputChange - The function to call when the input value changes.
 * @param {function} props.onSend - The function to call when the send button is clicked or Enter key is pressed.
 * @param {string} props.status - The current status of the chat input, which can be "submitted" or "streaming".
 * 
 * @returns {JSX.Element} The rendered chat input component.
 */
export const ChatInput = React.memo(({ input, onInputChange, onSend, status }: ChatInputProps) => {
  ChatInput.displayName = "ChatInput";

  const isSending = status === "submitted" || status === "streaming";
  const hasInput = input.trim() !== "";

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
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            onSend();
          }
        }}
      />
      {hasInput && (
        <button
          onClick={onSend}
          disabled={isSending || !hasInput}
          className={`
          flex items-center justify-center
          w-10 h-10
          rounded-full
          transition-colors duration-300
          ${
            !hasInput || isSending
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
});
