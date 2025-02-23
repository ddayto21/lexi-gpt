/**
 * A utility class for logging messages and errors in a structured and readable format.
 *
 * This logger:
 * - Outputs logs with proper indentation and colors for readability.
 * - Sends logs to a remote server (`http://localhost:4000/log`) for persistent storage.
 * - Groups logs to avoid cluttering the console.
 *
 * Usage:
 * - `Logger.log("User logged in", { userId: 123 })`
 * - `Logger.error("API request failed", errorObject)`
 *
 * @class
 */
export class Logger {
  /**
   * Logs a message with optional metadata in a structured, readable format.
   *
   * @static
   * @param {string} message - The log message.
   * @param {unknown} [data=null] - Optional metadata or context for the log.
   */
  static log(message: string, data: unknown = null) {
    const timestamp = new Date().toISOString();

    console.groupCollapsed(`📜 %c[LOG] ${timestamp}`, "color: green; font-weight: bold");
    console.log(`🔹 Message: %c${message}`, "color: #3498db; font-weight: bold;");
    if (data) {
      console.log("🔍 Data:", data);
    }
    console.groupEnd();

    Logger.sendToServer("LOG", message, data);
  }

  /**
   * Logs an error message with optional error details.
   *
   * @static
   * @param {string} message - The error message.
   * @param {unknown} [error=null] - Optional error details.
   */
  static error(message: string, error: unknown = null) {
    const timestamp = new Date().toISOString();

    console.groupCollapsed(`❌ %c[ERROR] ${timestamp}`, "color: red; font-weight: bold");
    console.log(`🔺 Error: %c${message}`, "color: #e74c3c; font-weight: bold;");
    if (error) {
      console.error("🛑 Details:", error);
    }
    console.groupEnd();

    Logger.sendToServer("ERROR", message, error);
  }

  /**
   * Sends the log entry to a remote logging server.
   *
   * This method is called internally by `log()` and `error()`
   * to persist logs remotely for debugging.
   *
   * @private
   * @static
   * @param {string} level - The log level (LOG, ERROR).
   * @param {string} message - The log message.
   * @param {unknown} data - Additional metadata for the log.
   */
  private static sendToServer(level: string, message: string, data: unknown) {
    fetch("http://localhost:4000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ level, message, data, timestamp: new Date().toISOString() }),
    }).catch((err) => console.error("🚨 Logging failed:", err));
  }
}

export const nonBlockingLog = (message: string, data?: unknown) => {
  setTimeout(() => {
    Logger.log(message, data);
  }, 0)
}