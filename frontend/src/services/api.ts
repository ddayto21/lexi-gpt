import type { SearchRequest, SearchResponse } from "../../types/api";

const BASE_URL = "https://main.d2hvd5sv2imel0.amplifyapp.com/api"

export async function searchBooks(query: string): Promise<SearchResponse> {
  console.log(`Searching for books with query: ${query}`);
  const payload: SearchRequest = { query };

  const response = await fetch(`${BASE_URL}/search_books`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch. Status: ${response.status}`);
  }

  const data: SearchResponse = await response.json();
  console.log("Raw JSON from backend:", data);
  // { recommendations: [ { title: "...", authors: [...], description: "..." } ] }
  return data;
}