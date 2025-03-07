import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

const API_BASE_URL = process.env.REACT_APP_BASE_URL;
if (!API_BASE_URL) {
  throw new Error("API_BASE_URL is not set");
}

/**
 * Props for the ProtectedRoute component.
 * @typedef {Object} ProtectedRouteProps
 * @property {React.JSX.Element} children - The protected content to render if authenticated.
 */
interface ProtectedRouteProps {
  children: React.JSX.Element;
}
/**
 * Protects routes by checking user authentication status.
 *
 * This component verifies if the user is authenticated by fetching their profile from the
 * backend. It redirects unauthenticated users to the login page and renders the protected
 * content only after confirming authentication. It includes a loading state to prevent
 * flickering and re-checks authentication when the window regains focus to handle OAuth
 * redirects correctly.
 *
 * @component
 * @param {ProtectedRouteProps} props - The properties passed to the component.
 * @returns {JSX.Element} The protected content or a redirect/navigation element.
 * @example
 * <ProtectedRoute><ChatPage /></ProtectedRoute>
 */
export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  /**
   * Checks the user's authentication status by querying the profile endpoint.
   *
   * Makes a GET request to `/auth/profile` with credentials included to verify session
   * cookies. Sets `isAuthenticated` based on the response. Re-runs on window focus to
   * catch session updates after OAuth redirects.
   */
  const checkAuth = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/auth/profile?ts=${Date.now()}`,
        {
          method: "GET",
          credentials: "include",
        }
      );
      setIsAuthenticated(response.ok);
    } catch (error) {
      console.error("Error checking authentication:", error);
      setIsAuthenticated(false);
    }
  };

  useEffect(() => {
    checkAuth();

    // Re-check auth when window regains focus (e.g., after OAuth redirect)
    const handleFocus = () => checkAuth();
    window.addEventListener("focus", handleFocus);
    return () => window.removeEventListener("focus", handleFocus);
  }, []);

  if (isAuthenticated === null) {
    return <div>Loading...</div>;
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
}
