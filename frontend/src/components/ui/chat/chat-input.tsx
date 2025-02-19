import React from "react";

interface ChatInputProps {
  input: string;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSend: () => void;
  status: string;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  input,
  onInputChange,
  onSend,
  status,
}) => (
  <footer className="flex items-center p-4 bg-neutral-900 border-t border-neutral-800">
    <input
      className="flex-1 px-4 py-2 rounded-full bg-neutral-800 text-gray-100 placeholder-gray-500 border border-neutral-700 focus:outline-none mr-2"
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
    <button
      onClick={onSend}
      disabled={status === "submitted" || input.trim() === ""}
      className="px-5 py-2 bg-blue-600 text-white rounded-full disabled:opacity-50 transition-colors"
    >
      Send
    </button>
  </footer>
);
