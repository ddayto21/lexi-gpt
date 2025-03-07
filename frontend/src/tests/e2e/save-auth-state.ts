/**
 * @file save-auth-state.ts
 * @description Utility to import pre-authenticated cookies and save them as a Playwright storage state.
 *
 * This script assumes you have manually logged into Google OAuth using a real Firefox browser
 * and exported cookies (e.g., via Cookie-Editor) to `cookies.json`. It loads those cookies
 * into a Playwright context and saves the state as `auth-state.json` for test reuse.
 *
 * @example
 *   npx ts-node src/tests/e2e/save-auth-state.ts
 */

import { firefox } from "playwright";
import { promises as fs } from "fs";

/**
 * @interface ExportedCookie
 * @description Shape of a cookie object exported from tools like Cookie-Editor.
 */
export interface ExportedCookie {
  name: string;
  value: string;
  domain?: string;
  path?: string;
  expires?: number;
  httpOnly?: boolean;
  secure?: boolean;
  sameSite?: string;
}

/**
 * @async
 * @function saveAuthState
 * @description Imports cookies from a JSON file and saves them as a Playwright storage state.
 * @returns {Promise<void>} Resolves when the storage state is saved and the browser is closed.
 */
export async function saveAuthState(): Promise<void> {
  // Launch a Firefox browser instance in headed mode.
  const browser = await firefox.launch({ headless: false });
  
  // Create a new browser context.
  const context = await browser.newContext();
  
  // Open a new page.
  const page = await context.newPage();
  
  // Load cookies from the exported file.
  const cookiesJson = await fs.readFile("src/tests/e2e/config/cookies.json", "utf-8");
  const cookies: ExportedCookie[] = JSON.parse(cookiesJson);
  
  // Convert cookies to Playwright's cookie format.
  const playwrightCookies = cookies.map((cookie: ExportedCookie) => ({
    name: cookie.name,
    value: cookie.value,
    domain: cookie.domain || "localhost",
    path: cookie.path || "/",
    expires: cookie.expires ? Math.floor(cookie.expires) : -1,
    httpOnly: cookie.httpOnly || false,
    secure: cookie.secure || false,
    // Ensure sameSite is one of "Lax", "Strict", or "None"
    sameSite: (cookie.sameSite as "Lax" | "Strict" | "None") || "Lax",
  }));
  await context.addCookies(playwrightCookies);
  
  // Navigate to the chat page to ensure cookies are applied.
  await page.goto("http://localhost:3000/chat");
  console.log("Navigated to chat page with imported cookies...");
  
  /**
   * Saves the browser's storage state (cookies, local storage) to a file.
   * @see {@link https://playwright.dev/docs/api/class-browsercontext#browser-context-storage-state|Playwright Storage State}
   */
  await context.storageState({ path: "src/tests/e2e/config/auth-state.json" });
  console.log("Saved authenticated state to src/tests/e2e/config/auth-state.json");
  
  // Close the browser.
  await browser.close();
}