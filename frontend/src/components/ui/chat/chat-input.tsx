import React from "react";
import { SendIcon } from "@components/icons/send-icon";
import { PauseIcon } from "@components/icons/pause-icon";

interface ChatInputProps {
  input: string;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSend: () => void;
  status: string; // "ready" | "submitted" | "error" etc.
}

export const ChatInput: React.FC<ChatInputProps> = ({
  input,
  onInputChange,
  onSend,
  status,
}) => {
  const isSending = status === "submitted" || status === "streaming";
  const hasInput = input.trim() !== "";

  return (
    <footer className="flex items-center p-4 bg-neutral-900 border-t border-neutral-800">
      <input
        className="
          flex-1
          px-4 py-2
          rounded-full
          bg-neutral-800 text-gray-100
          placeholder-gray-500
          border border-neutral-700
          focus:outline-none
          mr-2
        "
        placeholder="Describe a book you are looking for..."
        value={input}
        onChange={onInputChange}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            onSend();
          }
        }}
      />

      {/* 
        Only render the button if there's user input.
        If the user is sending, show disabled styling and a pause icon.
      */}
      {hasInput && (
        <button
          onClick={onSend}
          disabled={isSending || !hasInput} // ✅ Disable when input is empty
          className={`
      flex items-center justify-center
      w-10 h-10
      rounded-full
      transition-colors
      ${
        !hasInput || isSending
          ? "bg-gray-700 text-gray-400 cursor-not-allowed"
          : "bg-blue-600 hover:bg-blue-500 text-white"
      }
    `}
        >
          {isSending ? <PauseIcon /> : <SendIcon />}
        </button>
      )}
    </footer>
  );
};
