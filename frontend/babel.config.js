/**
 * Babel configuration file.
 *
 * This configuration tells Babel how to transform the code. It uses a set of presets to
 * transpile modern JavaScript, JSX, and TypeScript into a format that is compatible with the
 * current Node environment (or browsers as needed).
 *
 * @module babel.config
 */
module.exports = {
  presets: [
    /**
     * @preset @babel/preset-env
     * Transpiles modern JavaScript (ES6+) into a version compatible with the current Node.js version.
     * The { targets: { node: "current" } } option ensures that the output code is optimized for the version
     * of Node.js currently running our tests or application.
     */
    ["@babel/preset-env", { targets: { node: "current" } }],
    
    /**
     * @preset @babel/preset-react
     * Transforms JSX syntax into JavaScript that can be interpreted by browsers or Node.js.
     * This preset is necessary for projects using React.
     */
    "@babel/preset-react",
    
    /**
     * @preset @babel/preset-typescript
     * Transforms TypeScript code into JavaScript.
     * This preset allows us to write our code in TypeScript while Babel handles the conversion to JavaScript.
     */
    "@babel/preset-typescript",
  ],
};