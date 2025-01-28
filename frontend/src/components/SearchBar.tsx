import React, { useState } from "react";

export const SearchBar: React.FC = () => {
  const [query, setQuery] = useState<string>("");

  return (
    <div style={styles.searchBarContainer}>
      <div style={styles.searchBar}>
        <span style={styles.icon}>📎</span>
        <span style={styles.icon}>🌍</span>
        <span style={styles.icon}>📂</span>
        <input
          type="text"
          placeholder="Describe a book you're interested in reading..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.searchInput}
        />
        <button style={styles.sendButton}>⬆️</button>
      </div>
    </div>
  );
};

const styles = {
  searchBarContainer: {
    display: "flex",
    justifyContent: "center",
    width: "100%",
  },
  searchBar: {
    display: "flex",
    alignItems: "center",
    background: "#1e1e1e",
    borderRadius: "50px",
    padding: "12px 15px",
    width: "100%",
    maxWidth: "500px",
    boxShadow: "0px 4px 8px rgba(255, 255, 255, 0.05)",
  },
  searchInput: {
    flex: 1,
    border: "none",
    background: "transparent",
    color: "#ffffff",
    fontSize: "16px",
    padding: "10px",
    outline: "none",
  },
  sendButton: {
    background: "#4caf50",
    color: "#ffffff",
    border: "none",
    borderRadius: "50%",
    width: "36px",
    height: "36px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontSize: "16px",
    cursor: "pointer",
    transition: "background 0.2s",
  },
  sendButtonHover: {
    background: "#3d8b40",
  },
  icon: {
    color: "#888",
    fontSize: "16px",
    marginRight: "10px",
  },
};

export default SearchBar;
