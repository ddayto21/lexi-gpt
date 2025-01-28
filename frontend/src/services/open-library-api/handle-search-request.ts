import { searchBySubjects } from "./client";
import { constructSubjectQuery } from "./construct-subject-query";

/**
 * Processes search form input and submits a request to the Open Library API.
 * @param {string[]} subjects - Array of subject terms entered by the user.
 * @param {string} booleanOperator - Boolean operator to combine subjects (e.g., "AND", "OR").
 * @param {number} [page=1] - Page number for pagination.
 * @param {number} [limit=10] - Number of results per page.
 * @returns {Promise<any>} - The search results from the Open Library API.
 */
export const handleSearchRequest = async (
  subjects: string[],
  booleanOperator: "AND" | "OR" = "AND",
  page: number = 1,
  limit: number = 10
): Promise<any> => {
  if (!subjects.length) {
    throw new Error("Please enter at least one subject.");
  }

  // Construct the query using the constructSubjectQuery utility
  const queryUrl = constructSubjectQuery(
    subjects,
    booleanOperator,
    page,
    limit
  );
  console.log(`Constructed Query URL: ${queryUrl}`);

  // Use searchBySubjects to fetch results
  const results = await searchBySubjects(
    subjects,
    booleanOperator,
    page,
    limit
  );
  return results;
};
