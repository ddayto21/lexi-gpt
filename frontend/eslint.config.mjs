import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginReact from "eslint-plugin-react";

/** @type {import('eslint').Linter.FlatConfig[]} */
export default [
  {
    files: ["**/*.{js,mjs,cjs,ts,jsx,tsx}"],
    ignores: [
      "node_modules",
      "build",
      "dist",
      "coverage",
      "public",
      "**/node_modules/**",
      "**/build/**",
      "**/build/static/**",
      "**/build/static/js/**",
      "**/dist/**",
      "**/coverage/**",
      "**/public/**",
      "**/*.min.js",
      "**/*.map"
    ]
  },
  { languageOptions: { globals: { ...globals.browser, ...globals.node } } },
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  pluginReact.configs.flat.recommended
];