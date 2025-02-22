/**
 * A utility class for logging messages and errors.
 *
 * This logger automatically logs messages to the console and sends them
 * to a remote logging server (`http://localhost:4000/log`) for persistent storage.
 *
 * Usage:
 * - `Logger.log("Some message")`
 * - `Logger.error("Something went wrong", errorObject)`
 *
 * @class
 */
class Logger {
  /**
   * Logs a message with an optional data object.
   *
   * This method:
   * - Adds a timestamp to the log.
   * - Outputs the log to the console.
   * - Sends the log entry to a remote logging server.
   *
   * @static
   * @param {string} message - The log message to record.
   * @param {unknown} [data=null] - Optional additional data to include in the log.
   */
  static log(message: string, data: unknown = null) {
    const logEntry = `[LOG] ${new Date().toISOString()} - ${message}`;
    console.log(logEntry, data);
    Logger.sendToServer(logEntry, data);
  }

  /**
   * Logs an error message with an optional error object.
   *
   * This method:
   * - Formats the log with an `[ERROR]` tag and timestamp.
   * - Outputs the error to the console.
   * - Sends the error log to the remote logging server.
   *
   * @static
   * @param {string} message - The error message to record.
   * @param {unknown} [error=null] - Optional error object to include in the log.
   */
  static error(message: string, error: unknown = null) {
    const logEntry = `[ERROR] ${new Date().toISOString()} - ${message}`;
    console.error(logEntry, error);
    Logger.sendToServer(logEntry, error);
  }

  /**
   * Sends the log entry to a remote logging server.
   *
   * This method is called internally by `log()` and `error()` to persist logs.
   * If the request fails, an error is logged to the console.
   *
   * @private
   * @static
   * @param {string} message - The log or error message being sent.
   * @param {unknown} data - The additional data associated with the log.
   */
  private static sendToServer(message: string, data: unknown) {
    fetch("http://localhost:4000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, data }),
    }).catch((err) => console.error("Logging failed", err));
  }
}

export default Logger;
