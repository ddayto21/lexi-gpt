import { searchBySubjects } from "../services/open-library-api/client";
import { constructSubjectQuery } from "../services/open-library-api/construct-subject-query";

/**
 * Submits a book search request to the Open Library API.
 * @param {string} input - A string of subject terms entered by the user, separated by spaces.
 * @param {string} booleanOperator - Boolean operator to combine subjects (e.g., "AND", "OR").
 * @param {number} [page=1] - Page number for pagination.
 * @param {number} [limit=10] - Number of results per page.
 * @returns {Promise<any>} - The search results from the Open Library API.
 */
export const submitBookSearchRequest = async (
  input: string,
  booleanOperator: "AND" | "OR" = "AND",
  page: number = 1,
  limit: number = 10
): Promise<any> => {
  // Split the input string into an array of subjects
  const subjects = input
    .split(" ")
    .map((subject) => subject.trim())
    .filter((subject) => subject.length > 0);

  if (!subjects.length) {
    throw new Error("Please enter at least one valid subject.");
  }

  const queryUrl = constructSubjectQuery(subjects, booleanOperator, page, limit);
  console.log(`Constructed Query URL: ${queryUrl}`);

  return await searchBySubjects(subjects, booleanOperator, page, limit);
};