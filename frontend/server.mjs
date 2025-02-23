import express from "express";
import fs from "fs";
import { fileURLToPath } from "url";
import path from "path";

import cors from "cors";

const app = express();

app.use(express.json({ limit: "10mb" })); // ⬅️ Increase the limit (adjust as needed)
app.use(express.urlencoded({ extended: true, limit: "10mb" })); // ⬅️ Handle large form submissions

app.use(cors());

/**
 * Path to the log file where incoming logs will be stored.
 * The log file is named `dev.log` and is located in the server's directory.
 * @constant {string}
 */
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const LOG_FILE = path.join(__dirname, "dev.log");
console.log(`Logging to: ${LOG_FILE}`);
/**
 * Middleware to parse incoming JSON request bodies.
 */


/**
 * Endpoint to receive log messages from clients (e.g., frontend applications).
 *
 * Clients send logs via a `POST` request containing a JSON payload with:
 * - `message` (string): The log message to be recorded.
 * - `data` (optional, any): Additional context or metadata.
 *
 * Logs are saved to `dev.log` with a timestamp.
 *
 * @name POST /log
 * @function
 * @param {express.Request} req - Express request object containing log details in the body.
 * @param {express.Response} res - Express response object to send back status.
 */
app.post("/log", (req, res) => {
  /**
   * Extracts log message and optional data from the request body.
   * @type {string} message - The log message.
   * @type {any} [data] - Additional metadata (optional).
   */
  const { message, data } = req.body;

  /**
   * Formats the log entry with a timestamp and the log message.
   * If additional data is provided, it is converted to a JSON string.
   * @type {string}
   */
  const logEntry = `${new Date().toISOString()} - ${message} ${
    data ? JSON.stringify(data) : ""
  }\n`;

  /**
   * Appends the log entry to `dev.log`.
   * If an error occurs while writing, it is logged to the console.
   */
  fs.appendFile(LOG_FILE, logEntry, (err) => {
    if (err) {
      console.error("Error writing to log file", err);
    }
  });

  // Send a 200 OK response to confirm the log was received
  res.sendStatus(200);
});

/**
 * Starts the logging server on port 4000.
 * This server listens for incoming log requests and stores them in `dev.log`.
 *
 * @constant {number} PORT - The port number on which the server runs.
 */
app.listen(4000, () => console.log("Logging server running on port 4000"));
