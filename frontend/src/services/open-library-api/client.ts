/**
 * OpenLibrary API Client
 * Provides functions to search for books, retrieve author details, and fetch book covers.
 */

import type {
  OpenLibraryBook,
  OpenLibrarySearchResponse,
} from "../../../types/open-library-api";
import { constructSubjectQuery } from "./construct-subject-query";

const BASE_URL = "https://openlibrary.org";

/**
 * Generic function to fetch data from Open Library API.
 * @param {string} url - The fully constructed API URL.
 * @returns {Promise<any>} - The parsed JSON response.
 */
export const fetchFromOpenLibrary = async (url: string): Promise<any> => {
  console.log(`Fetching: ${url}`);
  const response = await fetch(url);
  
  console.log(`Response: ${response.status} ${response.statusText}`);
  if (!response.ok) throw new Error(`API Request Failed: ${response.statusText}`);
  return response.json(); // Parse and return JSON
};

/**
 * Searches for books in the Open Library API with optional parameters.
 * @param {string} query - Search query (title, author, or keywords).
 * @param {number} [page=1] - Page number for pagination.
 * @param {number} [limit=10] - Number of results per page.
 * @param {string} [language] - ISO 639-1 language code.
 * @param {boolean} [availability=false] - Whether to include availability data.
 * @returns {Promise<OpenLibrarySearchResponse>} - The search results.
 */
export const searchBooks = async (
  query: string,
  page: number = 1,
  limit: number = 10,
  language?: string,
  availability: boolean = false
): Promise<OpenLibrarySearchResponse> => {
  if (!query.trim()) throw new Error("Query cannot be empty.");

  let url = constructSubjectQuery([query], "AND", page, limit);
  console.log(`constructed url: ${url}`);

  if (language) url += `&lang=${language}`;
  if (availability) url += `&fields=*,availability`;

  return fetchFromOpenLibrary(url);
};

/**
 * Searches for books based on multiple subjects.
 * @param {string} input - The user-provided input string (space-separated subjects).
 * @param {string} [booleanOperator="AND"] - Boolean operator to combine subjects.
 * @param {number} [page=1] - Page number for pagination.
 * @param {number} [limit=10] - Number of results per page.
 * @returns {Promise<any>} - The search results.
 */
export const searchBySubjects = async (
  input: string,
  booleanOperator: "AND" | "OR" = "AND",
  page: number = 1,
  limit: number = 10
): Promise<any> => {
  const subjects = input
    .split(" ")
    .map((subject) => subject.trim())
    .filter((subject) => subject.length > 0);

  if (!subjects.length)
    throw new Error("At least one subject must be provided.");

  const url = constructSubjectQuery(subjects, booleanOperator, page, limit);
  return fetchFromOpenLibrary(url);
};

/**
 * Fetches a book cover image using Open Library ID (OLID).
 * @param {string} olid - The Open Library ID of the book.
 * @param {"S" | "M" | "L"} size - The desired cover size.
 * @returns {string} - The book cover image URL.
 */
export const getBookCover = (
  olid: string,
  size: "S" | "M" | "L" = "M"
): string => `https://covers.openlibrary.org/b/olid/${olid}-${size}.jpg`;

/**
 * Searches for authors in the Open Library API.
 * @param {string} query - The author's name.
 * @returns {Promise<any>} - The search results.
 */
export const searchAuthors = async (query: string): Promise<any> => {
  const url = `${BASE_URL}/search/authors.json?q=${encodeURIComponent(query)}`;
  return fetchFromOpenLibrary(url);
};

/**
 * Retrieves edition details for a given work.
 * @param {string} workKey - The Open Library Work Key (e.g., `/works/OL166894W`).
 * @returns {Promise<any>} - The edition details.
 */
export const getEditions = async (workKey: string): Promise<any> => {
  const url = `${BASE_URL}${workKey}/editions.json`;
  return fetchFromOpenLibrary(url);
};
