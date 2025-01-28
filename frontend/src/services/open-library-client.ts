/**
 * OpenLibrary API Client
 * Provides functions to search for books, retrieve author details, and fetch book covers.
 */

const BASE_URL = "https://openlibrary.org";

/**
 * Represents a book returned by the Open Library API.
 */
export interface Book {
  cover_i?: number;
  has_fulltext?: boolean;
  edition_count?: number;
  title: string;
  author_name?: string[];
  first_publish_year?: number;
  key: string;
  author_key?: string[];
  public_scan_b?: boolean;
}

/**
 * Represents the API response structure for a book search.
 */
export interface BookSearchResponse {
  start: number;
  num_found: number;
  docs: Book[];
}

/**
 * Searches for books in the Open Library API.
 * @param {string} query - The search query (title, author, or general keywords).
 * @param {number} [page=1] - The page number for pagination.
 * @returns {Promise<BookSearchResponse>} - A promise that resolves to book search results.
 */
export const searchBooks = async (
  query: string,
  page: number = 1
): Promise<BookSearchResponse> => {
  const url = `${BASE_URL}/search.json?q=${encodeURIComponent(query)}&page=${page}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("Failed to fetch books from Open Library.");
  }
  return response.json();
};

/**
 * Fetches book cover image using the Open Library ID (OLID).
 * @param {string} olid - The Open Library ID of the book.
 * @param {"S" | "M" | "L"} size - The desired cover size (S = Small, M = Medium, L = Large).
 * @returns {string} - The URL of the book cover image.
 */
export const getBookCover = (olid: string, size: "S" | "M" | "L" = "M"): string => {
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