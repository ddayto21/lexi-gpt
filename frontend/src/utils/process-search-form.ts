  
/**
 * Processes the search form input by splitting the input string into an array of words.
 * @param {string} input - A string of text describing a particular book subject.
 * @returns {string[]} - Array of extracted subjects.
 */
export const processSearchForm = (input: string): string[] => {
  const subjects = input
    .split(" ")
    .map((subject) => subject.trim())
    .filter((subject) => subject.length > 0);

  if (!subjects.length) {
    throw new Error("Please enter at least one valid subject.");
  }

  console.log(`Processed subjects: ${subjects}`);
  return subjects;
};

