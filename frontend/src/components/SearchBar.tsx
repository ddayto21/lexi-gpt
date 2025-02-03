import React, { useState } from "react";

interface SearchBarProps {
  onSearch: (query: string) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [input, setInput] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const handleSubmit = () => {
    if (input.trim() && !isSubmitting) {
      setIsSubmitting(true);
      console.log(`Submitting search query: ${input}`);
      onSearch(input);
      setTimeout(() => setIsSubmitting(false), 500); 
    }
  };

  return (
    <div style={styles.searchBarContainer}>
      <div style={styles.searchBar}>
        <span style={styles.icon}>📎</span>
        <span style={styles.icon}>🌍</span>
        <span style={styles.icon}>📂</span>
        <input
          type="text"
          placeholder="Describe a book you're interested in reading..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()} 

          style={styles.searchInput}
        />
        <button
          onClick={handleSubmit}
          disabled={isSubmitting} 
          style={styles.sendButton}
        >
          ⬆️
        </button>
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
  icon: {
    color: "#888",
    fontSize: "16px",
    marginRight: "10px",
  },
};

export default SearchBar;