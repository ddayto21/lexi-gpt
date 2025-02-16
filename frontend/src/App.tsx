// frontend/src/App.tsx
import React, { useState } from "react";
import { CSSProperties } from "react";
import { FaArrowUp } from "react-icons/fa";
import { StreamComponent } from "./components/StreamComponent";

// Represents a single message in the conversation log.
interface Message {
  role: "user" | "assistant";
  content: string;
}

const App: React.FC = () => {
  const [query, setQuery] = useState("");
  // Holds the submitted query that will be sent to the API.
  const [submittedQuery, setSubmittedQuery] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  // The index of the assistant message being updated.
  const [activeAssistantIndex, setActiveAssistantIndex] = useState<
    number | null
  >(null);

  // Disable button if input is empty or if a response is already loading.
  const isDisabled = !query.trim() || isLoading;

  const handleSend = () => {
    if (!query.trim() || isLoading) return;
    const trimmedQuery = query.trim();
    // Save the submitted query.
    setSubmittedQuery(trimmedQuery);
    // Append both the user message and a new empty assistant message in one call.
    setMessages((prev) => {
      const newMessages: Message[] = [
        ...prev,
        { role: "user", content: trimmedQuery },
        { role: "assistant", content: "" },
      ];
      // Set activeAssistantIndex to the index of the new assistant message.
      setActiveAssistantIndex(newMessages.length - 1);
      return newMessages;
    });
    setIsLoading(true);
    setQuery(""); // Clear the input field.
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  // Called on each update from the stream to update the current assistant message.
  const handleStreamUpdate = (partialText: string) => {
    if (activeAssistantIndex === null) return;
    setMessages((prev) => {
      const newMsgs = [...prev];
      newMsgs[activeAssistantIndex] = {
        ...newMsgs[activeAssistantIndex],
        content: partialText,
      };
      return newMsgs;
    });
  };

  // Called when the stream completes; reset loading state and active assistant index.
  const handleStreamComplete = () => {
    setIsLoading(false);
    setActiveAssistantIndex(null);
  };
  return (
    <div style={styles.appContainer}>
      <header style={styles.header}>
        <h1 style={styles.headerTitle}>Book Search Chat</h1>
      </header>

      <div style={styles.chatContainer}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={
              msg.role === "user"
                ? styles.userBubbleContainer
                : styles.assistantBubbleContainer
            }
          >
            <div
              style={
                msg.role === "user" ? styles.userBubble : styles.assistantBubble
              }
            >
              {msg.content}
            </div>
          </div>
        ))}

        {/* Render StreamComponent only if loading and submittedQuery exists */}
        {isLoading && submittedQuery && (
          <StreamComponent
            query={submittedQuery}
            onStreamUpdate={handleStreamUpdate}
            onStreamComplete={handleStreamComplete}
          />
        )}
      </div>

      <div style={styles.inputContainer}>
        <input
          type="text"
          placeholder="Send a message..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          style={styles.input}
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          style={{
            ...styles.sendButton,
            backgroundColor: isDisabled ? "#565869" : "#10a37f",
            cursor: isDisabled ? "not-allowed" : "pointer",
          }}
          disabled={isDisabled}
        >
          <FaArrowUp
            style={{
              fontSize: "1.2rem",
              color: isDisabled ? "#9ca0a6" : "#fff",
            }}
          />
        </button>
      </div>
    </div>
  );
};

const styles: { [key: string]: CSSProperties } = {
  appContainer: {
    display: "flex",
    flexDirection: "column",
    height: "100vh",
    backgroundColor: "#343541",
    color: "#ffffff",
    fontFamily: "Inter, sans-serif",
    overflow: "hidden",
  },
  header: {
    padding: "1rem",
    backgroundColor: "#202123",
    textAlign: "center",
  },
  headerTitle: {
    fontSize: "24px",
    fontWeight: "bold",
    margin: 0,
  },
  chatContainer: {
    flex: 1,
    overflowY: "auto",
    padding: "1rem",
    backgroundColor: "#343541",
  },
  userBubbleContainer: {
    display: "flex",
    justifyContent: "flex-end",
    marginBottom: "0.5rem",
  },
  userBubble: {
    backgroundColor: "#10a37f",
    padding: "0.75rem 1rem",
    borderRadius: "1rem",
    maxWidth: "70%",
    whiteSpace: "pre-wrap",
  },
  assistantBubbleContainer: {
    display: "flex",
    justifyContent: "flex-start",
    marginBottom: "0.5rem",
  },
  assistantBubble: {
    backgroundColor: "#444654",
    padding: "0.75rem 1rem",
    borderRadius: "1rem",
    maxWidth: "70%",
    whiteSpace: "pre-wrap",
  },
  inputContainer: {
    display: "flex",
    padding: "1rem",
    backgroundColor: "#202123",
  },
  input: {
    flex: 1,
    padding: "0.75rem",
    fontSize: "1rem",
    borderRadius: "4px",
    border: "1px solid #555",
    backgroundColor: "#3c3f41",
    color: "#fff",
    marginRight: "0.5rem",
    outline: "none",
  },
  sendButton: {
    width: "40px",
    height: "40px",
    borderRadius: "50%",
    border: "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
};

export default App;
