/**
 * OpenLibrary API Client
 * Provides functions to search for books, retrieve author details, and fetch book covers.
 */

import type { Book, BookSearchResponse } from "../../../types/open-library-api";
import { constructSubjectQuery } from "./construct-subject-query";

const BASE_URL = "https://openlibrary.org/search.json";
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

  const url = constructSubjectQuery(
    [query], // Use the query as the subject
    "AND",
    page,
    limit
  );

  if (language) url.concat(`&lang=${language}`);
  if (availability) url.concat(`&fields=*,availability`);

  const response = await fetch(url);
  if (!response.ok) throw new Error("Failed to fetch books from Open Library.");
  return response.json();
};

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
