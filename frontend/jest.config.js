/**
 * @file jest.config.js
 * @description Jest configuration that excludes Playwright e2e tests from being run.
 *
 * This configuration defines two projects:
 * - A "node" project for non-React tests (e.g. tests written in TypeScript)
 * - A "jsdom" project for React tests (TSX files)
 *
 * The testPathIgnorePatterns option below ensures that any files in the "src/tests/e2e/" directory
 * are not executed by Jest.
 */

module.exports = {
  // Ignore node_modules and the e2e folder (using <rootDir> for absolute path).
  testPathIgnorePatterns: ["/node_modules/", "/src/tests/e2e/"],
  
  projects: [
    {
      displayName: "node",
      preset: "ts-jest",
      testEnvironment: "node",
      testMatch: ["**/tests/**/*.test.ts"],
    },
    {
      displayName: "jsdom",
      testEnvironment: "jsdom",
      testMatch: ["**/tests/**/*.test.tsx", "**/src/tests/**/*.test.tsx"],
      transform: {
        "^.+\\.[tj]sx?$": "babel-jest",
      },
      transformIgnorePatterns: ["node_modules/(?!(react-markdown|remark-gfm)/)"],
      globals: {
        "ts-jest": { useESM: true },
      },
      extensionsToTreatAsEsm: [".ts", ".tsx", ".js", ".jsx"],
    },
  ],
};