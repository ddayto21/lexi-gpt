import type { Book } from "../../types/api";

const BASE_URL = "http://localhost:8000";

/**
 * Fetch book recommendations based on a natural language query.
 * @param {string} query - The user's search query.
 * @returns {Promise<object>} - The response data containing book recommendations.
 */
export const searchBooks = async (query: string): Promise<Book[]> => {
  const response = await fetch(`${BASE_URL}/search-books`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to fetch books.");
  }

  return response.json();
};
