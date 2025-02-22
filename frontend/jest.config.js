/**
 * Jest configuration file.
 *
 * This configuration defines two separate projects:
 *
 * 1. The "node" project is used for running tests written in TypeScript (non-React tests)
 *    in a Node.js environment using ts-jest.
 *
 * 2. The "jsdom" project is used for running React tests (TSX files) in a browser-like (jsdom)
 *    environment. It leverages babel-jest to transform both JavaScript and TypeScript files,
 *    including specific node_modules (react-markdown and remark-gfm) that are distributed as ESM.
 *
 * The configuration also specifies settings for handling ES modules via the `globals` and
 * `extensionsToTreatAsEsm` options.
 *
 * @module jest.config
 */
module.exports = {
  projects: [
    {
      /**
       * Node project configuration for non-React tests.
       *
       * @property {string} displayName - The name displayed for this project in test outputs.
       * @property {string} preset - The Jest preset to use (ts-jest) for transforming TypeScript files.
       * @property {string} testEnvironment - The environment in which to run tests (node).
       * @property {Array<string>} testMatch - Glob patterns specifying the test files for this project.
       */
      displayName: "node",
      preset: "ts-jest",
      testEnvironment: "node",
      testMatch: ["**/tests/**/*.test.ts"],
      
    },
    {
      /**
       * Jsdom project configuration for React tests.
       *
       * @property {string} displayName - The name displayed for this project in test outputs.
       * @property {string} testEnvironment - The environment in which to run tests (jsdom for browser-like testing).
       * @property {Array<string>} testMatch - Glob patterns specifying the test files for React components.
       * @property {Object} transform - Transformation configuration specifying that files with .ts, .tsx, .js, and .jsx extensions are transformed using babel-jest.
       * @property {Array<string>} transformIgnorePatterns - Patterns specifying which modules to ignore during transformation.
       *    In this case, react-markdown and remark-gfm are excluded from being ignored so they are transformed.
       * @property {Object} globals - Global configuration for ts-jest. Here it is set to use ESM.
       * @property {Array<string>} extensionsToTreatAsEsm - File extensions that should be treated as ES modules.
       */
      displayName: "jsdom",
      testEnvironment: "jsdom",
      testMatch: ["**/tests/**/*.test.tsx", "**/src/tests/**/*.test.tsx"],
      transform: {
        "^.+\\.[tj]sx?$": "babel-jest",
      },
      transformIgnorePatterns: [
        "node_modules/(?!(react-markdown|remark-gfm)/)",
      ],
      globals: {
        "ts-jest": {
          useESM: true,
        },
      },
      extensionsToTreatAsEsm: [".ts", ".tsx", ".js", ".jsx"],
    },
  ],
};
