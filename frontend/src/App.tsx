import React, { useState } from "react";
import { SearchBar } from "./components/SearchBar";
import { searchBooks } from "./services/api";
import type { Book } from "../types/api";

const App: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]); // State to store book recommendations
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const recommendations = await searchBooks(query); // Call the API service
      setBooks(recommendations); // Update the state with book recommendations
    } catch (err) {
      setError((err as Error).message || "Something went wrong!");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Book Finder</h1>
        <SearchBar onSearch={handleSearch} />
        {isLoading && <p>Loading...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
        <div>
          {books.map((book, index) => (
            <div
              key={index}
              style={{
                margin: "10px",
                border: "1px solid #ddd",
                padding: "10px",
              }}
            >
              <h3>{book.title}</h3>
              <p>
                <strong>Author:</strong> {book.author}
              </p>
              <p>
                <strong>Summary:</strong> {book.summary}
              </p>
            </div>
          ))}
        </div>
      </header>
    </div>
  );
};

export default App;
