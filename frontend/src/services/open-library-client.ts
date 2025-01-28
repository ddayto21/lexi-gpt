/**
 * OpenLibrary API Client
 * Provides functions to search for books, retrieve author details, and fetch book covers.
 */

const BASE_URL = "https://openlibrary.org";
import type { Book, BookSearchResponse } from "../../types/open-library-api";

/**
 * Searches for books in the Open Library API with optional parameters.
 * @param {string} query - Search query (title, author, or general keywords).
 * @param {number} [page=1] - Page number for pagination.
 * @param {number} [limit=10] - Number of results per page.

 * @param {string} [language] - Two-letter language code (ISO 639-1).
 * @param {boolean} [availability=false] - Whether to include availability data.
 * @returns {Promise<BookSearchResponse>} - A promise that resolves to book search results.
 */
export const searchBooks = async (
  query: string,
  page: number = 1,
  limit: number = 10,

  language?: string,
  availability: boolean = false
): Promise<BookSearchResponse> => {
  if (!query.trim()) throw new Error("Query cannot be empty.");

  const params = new URLSearchParams({
    q: query,
    page: page.toString(),
    limit: limit.toString(),
  });

  if (language) params.append("lang", language);
  if (availability) params.append("fields", "*,availability");

  const url = `${BASE_URL}/search.json?${params.toString()}`;
  console.log(`url: ${url}`);
  const response = await fetch(url);
  if (!response.ok) throw new Error("Failed to fetch books from Open Library.");
  return response.json();
};

/**
 * Fetches book cover image using the Open Library ID (OLID).
 * @param {string} olid - The Open Library ID of the book.
 * @param {"S" | "M" | "L"} size - The desired cover size (S = Small, M = Medium, L = Large).
 * @returns {string} - The URL of the book cover image.
 */
export const getBookCover = (
  olid: string,
  size: "S" | "M" | "L" = "M"
): string => {
  return `https://covers.openlibrary.org/b/olid/${olid}-${size}.jpg`;
};

/**
 * Searches for authors in the Open Library API.
 * @param {string} query - The author's name.
 * @returns {Promise<any>} - A promise resolving to the author search results.
 */
export const searchAuthors = async (query: string): Promise<any> => {
  const url = `${BASE_URL}/search/authors.json?q=${encodeURIComponent(query)}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("Failed to fetch authors from Open Library.");
  }
  return response.json();
};

/**
 * Retrieves edition details for a given work.
 * @param {string} workKey - The Open Library Work Key (e.g., `/works/OL166894W`).
 * @returns {Promise<any>} - A promise resolving to the edition details.
 */
export const getEditions = async (workKey: string): Promise<any> => {
  const url = `${BASE_URL}${workKey}/editions.json`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("Failed to fetch book editions.");
  }
  return response.json();
};
