/**
 * @file playwright.config.ts
 * @description Configuration for Playwright tests.
 *
 * This file sets up global testing parameters including:
 * - Test directory location
 * - Timeouts and retry settings
 * - Default base URL and screenshot capture policy
 * - Browser-specific project configurations (Chromium, Firefox, WebKit)
 */

import { defineConfig, devices } from "@playwright/test";
import * as dotenv from "dotenv";
import * as path from "path";

// Load environment variables from frontend/.env
dotenv.config({ path: path.resolve(__dirname, ".env") });

export default defineConfig({
  testDir: "./src/tests/e2e", // Directory where tests will reside

  timeout: 30000, // Global timeout for each test in milliseconds
  retries: 2, // Retry flaky tests up to 2 times
  expect: {
    timeout: 5000, // Timeout for expect assertions in milliseconds
  },
  use: {
    baseURL: "http://localhost:3000", // Base URL for all tests
    screenshot: "only-on-failure", // Capture screenshots only on test failure
  },
  projects: [
    {
      name: "Chromium",
      use: { ...devices["Desktop Chrome"] }, // Use Desktop Chrome configuration for Chromium
    },
    {
      name: "Firefox",
      use: { ...devices["Desktop Firefox"] }, // Use Desktop Firefox configuration for Firefox
    },
    {
      name: "WebKit",
      use: { ...devices["Desktop Safari"] },
    },
  ],
});
