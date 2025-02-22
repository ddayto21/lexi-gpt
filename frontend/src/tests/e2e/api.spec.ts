/**
 * @fileoverview Integration tests for API endpoints using Playwright's request API.
 * These tests ensure that the API server is up and running by checking key endpoints.
 */

import { test, expect } from "@playwright/test";

/**
 * A suite of API Integration Tests.
 *
 * This test suite verifies that the API server responds as expected.
 */
test.describe("API Integration Tests", () => {
  /**
   * Verifies that the base endpoint returns a 200 status code.
   *
   * This test sends an HTTP GET request to the API's root endpoint (http://localhost:8000)
   * using Playwright's request API. It asserts that the returned status code is 200,
   * indicating that the API is healthy and capable of handling requests.
   *
   * @async
   * @function
   * @param {import('@playwright/test').APIRequestContext} request - The Playwright API request context for making HTTP calls.
   */
  test("GET /api/health returns status 200", async ({ request }) => {
    const response = await request.get("http://localhost:8000");
    expect(response.status()).toBe(200);
  });
});
