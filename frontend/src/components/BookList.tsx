import React from "react";
import type { Book } from "../../types/api";

interface BookListProps {
  books: Book[];
}

export const BookList: React.FC<BookListProps> = ({ books }) => {
  return (
    <div style={styles.resultsContainer}>
      {books.map((book, index) => (
        <div key={index} style={styles.bookCard}>
          <h3>{book.title}</h3>
          <p>
            <strong>Author:</strong> {book.author_name?.join(", ") || "N/A"}
          </p>
        </div>
      ))}
    </div>
  );
};

const styles = {
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

export default BookList;
