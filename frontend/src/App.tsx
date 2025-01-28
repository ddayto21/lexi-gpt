import React, { useState } from "react";
import { SearchBar } from "./components/SearchBar";
import type { Book } from "../types/api";

const App: React.FC = () => {
  return (
    <div style={styles.appContainer}>
      <h1 style={styles.title}>Search for a book</h1>
      <SearchBar />
    </div>
  );
};

import { CSSProperties } from "react";

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
  actionButtons: {
    display: "flex",
    gap: "10px",
    marginTop: "20px",
  },
  actionButton: {
    backgroundColor: "#1e1e1e",
    color: "#ffffff",
    border: "none",
    borderRadius: "20px",
    padding: "10px 15px",
    fontSize: "14px",
    cursor: "pointer",
    transition: "background 0.2s ease-in-out, transform 0.2s ease-in-out",
  },
};

export default App;
