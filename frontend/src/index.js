/**
 * @file Entry point of the React application.
 *
 * This file initializes the React app, mounts the `App` component to the DOM,
 * and enables global logging for API requests. It also includes an optional
 * performance monitoring function (`reportWebVitals`).
 */
import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css"; // Import global styles
import App from "./App"; // Main application component
import reportWebVitals from "./reportWebVitals"; // Performance monitoring utility

// Enable global fetch logging for API requests
// import "./setupFetchLogger";

/**
 * The root element where the React application is mounted.
 *
 * Uses `ReactDOM.createRoot()` to enable React's Concurrent Mode.
 *
 * @constant {ReactDOM.Root}
 */
const root = ReactDOM.createRoot(document.getElementById("root"));
/**
 * Renders the main `App` component inside a React Strict Mode wrapper.
 *
 * - `StrictMode` helps with identifying potential problems in the app during development.
 */
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

/**
 * Reports web performance metrics for the application.
 *
 * - You can pass a logging function to measure performance data (e.g., `console.log`).
 * - Alternatively, send performance data to an analytics endpoint.
 *
 * Learn more: {@link https://bit.ly/CRA-vitals}
 */ reportWebVitals();
