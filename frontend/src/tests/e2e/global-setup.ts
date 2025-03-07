/**
 * @file global-setup.ts
 * @description Global setup for Playwright e2e tests.
 *
 * This file runs once before any tests execute. It calls the saveAuthState utility
 * to generate the pre-authenticated storage state (auth-state.json) for test reuse.
 */

import { saveAuthState } from "./save-auth-state";

// Export a default function (as required by Playwright) that runs global setup.
export default async function globalSetup(): Promise<void> {
  await saveAuthState();
}