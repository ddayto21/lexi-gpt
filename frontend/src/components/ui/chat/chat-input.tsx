import React from "react";
import { SendIcon } from "@components/icons/send-icon";
import { PauseIcon } from "@components/icons/pause-icon";
import { nonBlockingLog } from "@utils/logger";

import { useChat } from "@ai-sdk/react";

export const ChatInput: React.FC = () => {
  const { input, status, handleSubmit, handleInputChange } = useChat({
    id: "chat",
  });
  const isSending = status === "submitted" || status === "streaming";
  const hasInput = input.trim() !== "";
  nonBlockingLog("📝 <ChatInput> component rendered");
  return (
    <footer className="flex items-center p-4 bg-neutral-900 border-t border-neutral-800">
      <input
        aria-label="Chat message input"
        role="textbox"
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
        onChange={handleInputChange}
        onKeyDown={handleSubmit}
      />

      <button
        type="submit"
        disabled={isSending || !hasInput} // ✅ Prevents sending empty messages
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
    </footer>
  );
};
