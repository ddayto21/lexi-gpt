/**
 * Saves a reference to the original `fetch` function before overriding it.
 */
const originalFetch = window.fetch;

/**
 * Overrides the global `fetch` function to automatically log all API requests and responses.
 *
 * This ensures every outgoing network request made via `fetch` is logged,
 * including request method, headers, body, and response details.
 * Useful for debugging and monitoring API interactions in real-time.
 *
 * @param {...any} args - The original arguments passed to `fetch`, including the request URL and options.
 * @returns {Promise<Response>} - A Promise resolving to the original `fetch` response object.
 */

window.fetch = async (...args) => {
  /** Extract the request URL and options */
  const [url, options] = args;

  /**
   * The HTTP method of the request (GET, POST, etc.).
   * Defaults to "GET" if no method is explicitly set.
   * @type {string}
   */
  const method = options?.method || "GET";

  /**
   * The request headers, defaulting to an empty object if none are provided.
   * @type {Object}
   */
  const headers = options?.headers || {};

  /**
   * The request body, stringified if present; otherwise, defaults to "N/A".
   * @type {string}
   */
  const body = options?.body ? JSON.stringify(options.body) : "N/A";

  console.log(`Making a ${method} request to ${url}`);
  console.log(`Request headers: ${JSON.stringify(headers)}`);
  console.log(`Request body: ${body}`);

  /**
   * Calls the original fetch function with the provided arguments.
   * This ensures that the request is still made as expected.
   * @type {Response}
   */

  const response = await originalFetch(...args);

  console.log(`Response from ${method} ${url}  (Status: ${response.status}) `);
  console.log(response);

  /** Return the original fetch response to maintain expected behavior */
  return response;
};
