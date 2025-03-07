/**
 * @file playwright.config.ts
 * @description Configuration for Playwright e2e tests.
 *
 * This file sets up global testing parameters including:
 * - Test directory location
 * - Timeouts and retry settings
 * - Default base URL and screenshot capture policy
 * - Browser-specific project configurations (e.g. Firefox in headed mode)
 * - Global setup to generate a pre-authenticated storage state.
 */

import { defineConfig, devices } from "@playwright/test";
import * as dotenv from "dotenv";
import * as path from "path";

// Load environment variables from the .env file.
dotenv.config({ path: path.resolve(__dirname, ".env") });

export default defineConfig({
  testDir: "./src/tests/e2e", // Directory where e2e tests reside
  globalSetup: require.resolve("./src/tests/e2e/global-setup.ts"),
  testMatch: ["**/*.{spec,test,e2e}.{js,ts,jsx,tsx}"],
  timeout: 100000, // Global test timeout in ms
  retries: 0,      // No retries
  expect: {
    timeout: 50000, // Timeout for expect assertions
  },
  use: {
    baseURL: "http://localhost:3000",
    screenshot: "only-on-failure",
    // Load the storage state to simulate an already authenticated session.
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