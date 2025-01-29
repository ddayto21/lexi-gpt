import { searchBySubjects } from "../services/open-library-api/client";
import { constructSubjectQuery } from "../services/open-library-api/construct-subject-query";

/**
 * Submits a book search request to the Open Library API.
 * @param {string[]} subjects - Array of subject terms extracted from the search form.
 * @param {string} booleanOperator - Boolean operator to combine subjects (e.g., "AND", "OR").
 * @param {number} [page=1] - Page number for pagination.
 * @param {number} [limit=10] - Number of results per page.
 * @returns {Promise<any>} - The search results from the Open Library API.
 */
export const submitBookSearchRequest = async (
  subjects: string[],
  booleanOperator: "AND" | "OR" = "AND",
  page: number = 1,
  limit: number = 10
): Promise<any> => {
  const queryUrl = constructSubjectQuery(
    subjects,
    booleanOperator,
    page,
    limit
  );
  console.log(`Constructed Query URL: ${queryUrl}`);

  return await searchBySubjects(subjects, booleanOperator, page, limit);
};
