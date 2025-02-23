import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./src/tests/e2e", // Directory where tests will live
  timeout: 30000, // Global timeout for each test in milliseconds
  expect: {
    timeout: 5000, // Timeout for expect assertions
  },
  use: {
    baseURL: "http://localhost:3000",
    // Capture screenshots on test failure
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "Chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "Firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "WebKit",
      use: { ...devices["Desktop Safari"] },
    },
  ],
});
