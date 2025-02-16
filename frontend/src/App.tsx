// src/App.tsx
import React, { useState } from "react";
import { StreamComponent } from "./components/StreamComponent";
import { CSSProperties } from "react";

const App: React.FC = () => {
  const [query, setQuery] = useState("");
  const [submittedQuery, setSubmittedQuery] = useState<string | null>(null);

  const handleSend = () => {
    if (query.trim()) {
      setSubmittedQuery(query.trim());
    }
  };

  return (
    <div style={styles.appContainer}>
      <header style={styles.header}>
        <h1>Book Search Chat</h1>
      </header>

      <div style={styles.chatContainer}>
        {submittedQuery ? (
          <StreamComponent query={submittedQuery} />
        ) : (
          <p>Type your query and click "Send" to get recommendations.</p>
        )}
      </div>

      <div style={styles.inputContainer}>
        <input
          type="text"
          placeholder="Search for a book..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
        />
        <button onClick={handleSend} style={styles.button}>
          Send
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
    backgroundColor: "#343541", // Dark background similar to ChatGPT dark mode.
    color: "#ffffff", // White text.
    fontFamily: "Inter, sans-serif",
    overflow: "hidden",
  },
  header: {
    padding: "1rem",
    backgroundColor: "#202123", // A darker header background.
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
  placeholderText: {
    color: "#c9c9c9",
    fontStyle: "italic",
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
  },
  button: {
    padding: "0.75rem 1.5rem",
    fontSize: "1rem",
    borderRadius: "4px",
    backgroundColor: "#0084ff",
    color: "#fff",
    border: "none",
    cursor: "pointer",
  },
};
export default App;
