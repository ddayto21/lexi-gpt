/**
 * @file playwright.config.ts
 * @description Configuration for Playwright tests.
 *
 * This file sets up global testing parameters including:
 * - Test directory location
 * - Timeouts and retry settings
 * - Default base URL and screenshot capture policy
 * - Browser-specific project configurations (e.g. Firefox in headed mode)
 */

import { defineConfig, devices } from "@playwright/test";
import * as dotenv from "dotenv";
import * as path from "path";

// Load environment variables from the .env file using __dirname (CommonJS variable).
dotenv.config({ path: path.resolve(__dirname, ".env") });

export default defineConfig({
  testDir: "./src/tests/e2e", // Directory where tests will reside
  timeout: 100000, // Global timeout for each test in milliseconds
  retries: 0, // Number of test retries
  expect: {
    timeout: 50000, // Timeout for expect assertions in milliseconds
  },
  use: {
    baseURL: "http://localhost:3000",
    screenshot: "only-on-failure",
    // Load the storage state (auth-state.json) to simulate an already authenticated session.
    storageState: "src/tests/e2e/config/auth-state.json",
  },
  projects: [
    {
      name: "Firefox",
      use: {
        ...devices["Desktop Firefox"],
        headless: false, // Run in headed mode
      },
    },
  ],
});