import { getTimeAgo } from "../../utils/parse-sse-data";
describe("getTimeAgo", () => {
    /**
     * Verifies that getTimeAgo returns an empty string when no timestamp is provided.
     */
    test("should return an empty string if no timestamp is provided", () => {
      expect(getTimeAgo()).toBe("");
    });
  
    /**
     * Verifies that getTimeAgo returns a relative time string for a valid timestamp.
     */
    test("should return a relative time string for a valid timestamp", () => {
      const now = new Date().toISOString();
      const result = getTimeAgo(now);
      expect(result).not.toBe("");
    });
  });
  
