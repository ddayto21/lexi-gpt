/**
 * OAuth configuration for Google login.
 * @constant {Object} authConfig
 * @property {string} clientId - Google OAuth client ID from environment variables.
 * @property {string} redirectUri - Backend callback URI for OAuth redirect.
 * @property {string} scope - Requested OAuth scopes (openid, email, profile).
 * @property {string} prompt - Forces account selection prompt.
 * @property {string} baseAuthUrl - Google OAuth base authorization URL.
 */

// Ensure required environment variables are set
if (!process.env.REACT_APP_GOOGLE_CLIENT_ID) {
  throw new Error("REACT_APP_GOOGLE_CLIENT_ID is not set");
}
if (!process.env.REACT_APP_REDIRECT_URI) {
  throw new Error("REACT_APP_REDIRECT_URI is not set");
}
if (!process.env.REACT_APP_BASE_URL) {
  throw new Error("REACT_APP_BASE_URL is not set");
}

export const authConfig = {
  clientId: process.env.REACT_APP_GOOGLE_CLIENT_ID!,
  redirectUri: `${process.env.REACT_APP_BASE_URL}/auth/callback`,
  scope: "openid email profile",
  prompt: "select_account",
  baseAuthUrl: "https://accounts.google.com/o/oauth2/v2/auth",
};
