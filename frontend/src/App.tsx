import React, { useState } from "react";
import { SearchBar } from "./components/SearchBar";
import type { Book } from "../types/api";
import { searchBySubjects } from "./services/open-library-api/client"
import { CSSProperties } from "react";

const App: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    setError(null);
    try {
      const results = await searchBySubjects(query);
      setBooks(results.docs || []);
    } catch (err) {
      setError(`Failed to fetch books: ${err} Please try again.`);
    }
  };

  return (
    <div style={styles.appContainer}>
      <h1 style={styles.title}>Search for a book</h1>
      <SearchBar onSearch={handleSearch} />
      {error && <p style={styles.error}>{error}</p>}
      <div style={styles.resultsContainer}>
        {books.map((book, index) => (
          <div key={index} style={styles.bookCard}>
            <h3>{book.title}</h3>
            <p>
              <strong>Author:</strong> {book.author_name?.join(", ") || "N/A"}
            </p>
            <p>
              <strong>First Published:</strong>{" "}
              {book.first_publish_year || "N/A"}
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
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    backgroundColor: "#0d0d0d",
    color: "#f0f0f0",
    fontFamily: "Inter, sans-serif",
  },
  title: {
    fontSize: "24px",
    fontWeight: "bold",
    marginBottom: "20px",
  },
  error: {
    color: "red",
    marginTop: "10px",
  },
  resultsContainer: {
    marginTop: "20px",
    width: "100%",
    maxWidth: "600px",
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