import React, { useState } from "react";
import { SearchBar } from "./components/SearchBar";
import type { Book } from "../types/api";
import { searchBooks } from "./services/api";
import { CSSProperties } from "react";

const App: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    setError(null);
    try {
      const data = await searchBooks(query);
      setBooks(data.recommendations || []);
    } catch (err: any) {
      setError(
        `Failed to fetch books: ${err?.message || err}. Please try again.`
      );
    }
  };

  return (
    <div style={styles.appContainer}>
      <h1 style={styles.title}>Search for a book</h1>

      {/* Fixed SearchBar */}
      <div style={styles.searchBarWrapper}>
        <SearchBar onSearch={handleSearch} />
      </div>

      {error && <p style={styles.error}>{error}</p>}

      {/* Scrollable results container */}
      <div style={styles.resultsContainer}>
        {books.map((book, index) => (
          <div key={index} style={styles.bookCard}>
            <h3>{book.title}</h3>
            <p>
              <strong>Author(s):</strong> {book.authors?.join(", ") || "N/A"}
            </p>
            <p>
              <strong>Description:</strong>{" "}
              {book.description || "No description"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles: { [key: string]: CSSProperties } = {
  appContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    height: "100vh",
    backgroundColor: "#0d0d0d",
    color: "#f0f0f0",
    fontFamily: "Inter, sans-serif",
    overflow: "hidden", // Prevents unwanted body scrolling
  },
  title: {
    fontSize: "24px",
    fontWeight: "bold",
    marginTop: "20px",
    marginBottom: "10px",
  },
  searchBarWrapper: {
    position: "sticky",
    top: "0",
    zIndex: 10, 
    backgroundColor: "#0d0d0d",
    width: "100%",
    display: "flex",
    justifyContent: "center",
    padding: "10px 0",
  },
  error: {
    color: "red",
    marginTop: "10px",
  },
  resultsContainer: {
    flex: 1,
    width: "100%",
    maxWidth: "600px",
    overflowY: "auto", 
    paddingTop: "10px",
  },
  bookCard: {
    backgroundColor: "#1e1e1e",
    padding: "15px",
    borderRadius: "10px",
    marginBottom: "10px",
    boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.5)",
  },
};

export default App;