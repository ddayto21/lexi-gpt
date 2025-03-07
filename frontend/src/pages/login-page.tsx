import React, { useCallback, useState } from "react";
import { FcGoogle } from "react-icons/fc";
import { Link } from "react-router-dom";
import { RAGProcess } from "@components/ui/features/rag-system";
import { authConfig } from "@config/auth-config";

/**
 * Renders the login page with Google OAuth integration and a demo section.
 *
 * This component provides a split-screen layout: a demo of the RAG process on the left
 * (visible on large screens) and a Google login form on the right. It constructs a Google
 * OAuth URL using environment variables and redirects the user to authenticate when the
 * login button is clicked. The component is optimized with memoization to prevent
 * unnecessary re-renders and includes accessibility attributes for better usability.
 *
 * @component
 * @returns {JSX.Element} The rendered login page.
 * @example
 * <LoginPage />
 */
export const LoginPage = React.memo(() => {
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Initiates Google OAuth authentication by redirecting to the authorization URL.
   *
   * Constructs the OAuth URL using the `authConfig` settings, encoding parameters for
   * security. Redirects the current window to the URL and sets a loading state for user
   * feedback. Used for both login and signup actions, as the Google flow handles account
   * creation if needed. Errors are logged for debugging.
   *
   * @function handleLogin
   */
  const handleLogin = useCallback(() => {
    setIsLoading(true);
    try {
      const { clientId, redirectUri, scope, prompt, baseAuthUrl } = authConfig;
      const authUrl = `${baseAuthUrl}?client_id=${clientId}&redirect_uri=${encodeURIComponent(
        redirectUri
      )}&response_type=code&scope=${encodeURIComponent(
        scope
      )}&access_type=offline&prompt=${prompt}`;
      window.location.href = authUrl; // Redirect in same window
    } catch (error) {
      console.error("Login redirect failed:", error);
      setIsLoading(false); // Reset loading on error
    }
  }, []);

  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-[#0a0a0a] text-white">
      {/* Left Side: Markdown Demo */}
      <div className="hidden lg:flex flex-col items-center justify-center p-8 bg-gradient-to-b from-blue-900 to-purple-900">
        <div className="w-full max-w-lg mx-auto space-y-12">
          <div className="max-w-full">
            <RAGProcess />
          </div>
        </div>
      </div>

      {/* Right Side: Login Form */}
      <div className="flex flex-col items-center justify-center p-8">
        <div className="w-full max-w-sm space-y-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 text-transparent bg-clip-text">
              LexiGPT
            </h1>
            <h2 className="text-xl text-gray-300 mt-2">Welcome Back</h2>
          </div>

          <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
            {/* Google Sign-In Button */}
            <button
              type="button"
              onClick={handleLogin}
              disabled={isLoading}
              aria-label="Log in with Google"
              className="flex items-center justify-center w-full p-3 rounded-full bg-white text-black font-medium text-lg transition hover:bg-gray-200 disabled:opacity-50"
            >
              <FcGoogle className="mr-2 text-2xl" />
              {isLoading ? "Logging in..." : "Log in with Google"}
            </button>

            {/* Divider */}
            <div className="relative text-center">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-700"></div>
              </div>
              <div className="relative inline-block px-2 bg-[#0a0a0a] text-gray-400">
                or
              </div>
            </div>

            <p className="text-center text-sm text-gray-400">
              Don’t have an account?{" "}
              <button
                type="button"
                onClick={handleLogin}
                disabled={isLoading}
                className="text-blue-500 hover:underline disabled:opacity-50"
              >
                Sign Up
              </button>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
});

LoginPage.displayName = "LoginPage";
