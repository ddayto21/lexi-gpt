/**
 * @file oauth-flow.e2e.ts
 * @description End-to-end test for verifying a pre-authenticated session using a saved storage state.
 *
 * This test uses a pre-saved authenticated storage state (auth-state.json) to verify that an already
 * logged-in session can access the chat page.
 */

import { test, expect } from "@playwright/test";

const BASE_URL = process.env.BASE_URL || "http://localhost:3000";

test.describe("Pre-authenticated session", () => {
  /**
   * @description Verifies that a user with a pre-authenticated state can access the chat page directly.
   */
  test("should load the chat page when navigating directly with a pre-authenticated state", async ({
    page,
  }) => {
    // Directly navigate to the chat page.
    await page.goto(`${BASE_URL}/chat`);
    await expect(page).toHaveURL(/\/chat$/);
    console.log("[Test] Chat page loaded with pre-authenticated state");

    // Verify key elements on the chat page.
    const header = page.locator("header"); // Adjust the selector as needed.
    await expect(header).toBeVisible();
    const profileName = page.locator("text=testuser"); // Adjust to match the expected profile name.
    await expect(profileName).toBeVisible();
  });
});