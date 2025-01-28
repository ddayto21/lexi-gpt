/**
 * OpenLibrary API Client
 * Provides functions to search for books, retrieve author details, and fetch book covers.
 */

import type { Book, BookSearchResponse } from "../../../types/open-library-api";

const BASE_URL = "https://openlibrary.org/search.json";

/**
 * Constructs a query string for the Open Library Subject Search API.
 * @param {string[]} subjects - Array of subject terms to search for.
 * @param {string} [booleanOperator="AND"] - Boolean operator to combine subjects (e.g., "AND", "OR").
 * @param {number} [page=1] - Page number for pagination.
 * @param {number} [limit=10] - Number of results per page.
 * @returns {string} - The constructed query string.
 */
const constructSubjectQuery = (
  subjects: string[],
  booleanOperator: "AND" | "OR" = "AND",
  page: number = 1,
  limit: number = 10
): string => {
  const URL = `${BASE_URL}/subjects.json`;
  const subjectQuery = subjects
    .map((subject) => `subject:${encodeURIComponent(subject)}`)
    .join(`+${booleanOperator}+`);

  const params = new URLSearchParams({
    q: subjectQuery,
    page: page.toString(),
    limit: limit.toString(),
  });

  return `${URL}?${params.toString()}`;
};

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
 * Fetches books from the Open Library Subject Search API using fuzzy matching and boolean logic.
 * @param {string[]} subjects - Array of subject terms to search for.
 * @param {string} [booleanOperator="AND"] - Boolean operator to combine subjects (e.g., "AND", "OR").
 * @param {number} [page=1] - Page number for pagination.
 * @param {number} [limit=10] - Number of results per page.
 * @returns {Promise<any>} - A promise that resolves to the search results from the Open Library API.
 */
export const searchBySubjects = async (
  subjects: string[],
  booleanOperator: "AND" | "OR" = "AND",
  page: number = 1,
  limit: number = 10
): Promise<any> => {
  if (!subjects.length) {
    throw new Error("At least one subject must be provided.");
  }

  const url = constructSubjectQuery(subjects, booleanOperator, page, limit);

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("Failed to fetch data from Open Library API.");
  }

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
