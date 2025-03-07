import React, { useState, useEffect, useRef } from "react";
import { AiAvatar } from "@components/ui/avatars/ai-avatar";

const API_BASE_URL = process.env.REACT_APP_BASE_URL;
if (!API_BASE_URL) {
  throw new Error("API_BASE_URL is not set");
}

/**
 * User profile data fetched from the API.
 * @typedef {Object} UserProfile
 * @property {string} [picture] - URL of the user's profile picture.
 * @property {string} [name] - User's display name.
 */
interface UserProfile {
  picture?: string;
  name?: string;
}

/**
 * Renders the chat application's header with user profile and menu options.
 *
 * This component displays a branded header with an AI avatar, app title, and a user profile
 * dropdown menu. It fetches the user's profile on mount, handles sign-out and data deletion
 * via API calls, and manages a dropdown menu that closes on outside clicks or resize. The
 * menu is dynamically positioned to stay within the viewport, and the component is optimized
 * with memoization to prevent unnecessary re-renders.
 *
 */
export const Header = React.memo(() => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const profileButtonRef = useRef<HTMLButtonElement>(null);

  /**
   * Fetches the user's profile data from the API on component mount.
   *
   * Makes a GET request to `/auth/profile` with credentials included. Checks the response
   * Content-Type to ensure it’s JSON before parsing. Updates `userProfile` with the data
   * if successful, or logs detailed errors if the response is invalid or non-JSON. Falls
   * back to null if parsing fails.
   */
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/auth/profile`, {
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(
            `HTTP error: ${response.status} ${response.statusText}`
          );
        }

        const contentType = response.headers.get("Content-Type");
        if (!contentType || !contentType.includes("application/json")) {
          const text = await response.text();
          console.error("Profile response is not JSON:", {
            contentType,
            body: text,
          });
          return; // Leave userProfile as null
        }

        const data = await response.json();
        setUserProfile(data.profile || data.user || null);
      } catch (error) {
        console.error("Failed to fetch user profile:", error);
      }
    };

    fetchUserProfile();
  }, []);

  /**
   * Toggles the visibility of the profile dropdown menu.
   * @param {React.MouseEvent} e - The click event on the profile button or name.
   */
  const handleProfileClick = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsMenuOpen((prev) => !prev);
  };

  /**
   * Signs the user out by calling the sign-out API and redirecting to the homepage.
   *
   * Sends a GET request to the sign-out endpoint. On success, redirects to the root URL.
   * Closes the menu regardless of outcome.
   */
  const handleSignOut = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/signout`, {
        method: "GET",
        credentials: "include",
      });
      if (response.ok) {
        window.location.href = "/";
      } else {
        console.error("Failed to sign out:", response.statusText);
      }
    } catch (error) {
      console.error("Sign out error:", error);
    }
    setIsMenuOpen(false);
  };

  /**
   * Deletes user data from the server cache via a DELETE request.
   *
   * Sends a DELETE request to the cache endpoint. Logs success or failure for debugging.
   * Closes the menu after execution.
   */
  const handleDeleteUserData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/cache`, {
        method: "DELETE",
        credentials: "include",
      });
      if (response.ok) {
        console.log("User data deleted from cache.");
      } else {
        console.error("Failed to delete user data:", response.statusText);
      }
    } catch (error) {
      console.error("Error deleting user data:", error);
    }
    setIsMenuOpen(false);
  };

  /**
   * Closes the menu when clicking outside the menu or profile button.
   *
   * Adds a mousedown listener when the menu is open, checking if the click target is outside
   * both the menu and button refs. Cleans up the listener on unmount or when the menu closes.
   */
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        menuRef.current &&
        profileButtonRef.current &&
        !menuRef.current.contains(event.target as Node) &&
        !profileButtonRef.current.contains(event.target as Node)
      ) {
        setIsMenuOpen(false);
      }
    };

    if (isMenuOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      return () =>
        document.removeEventListener("mousedown", handleClickOutside);
    }
  }, [isMenuOpen]);

  /**
   * Positions the dropdown menu to stay within the viewport.
   *
   * Calculates the menu's position based on the profile button's bounding rect, placing it
   * below the button unless it would overflow the viewport, then positioning it above.
   * Runs on menu open and window resize.
   */
  const positionMenu = () => {
    if (menuRef.current && profileButtonRef.current) {
      const buttonRect = profileButtonRef.current.getBoundingClientRect();
      const menu = menuRef.current;
      const viewportHeight = window.innerHeight;

      let top = buttonRect.bottom + 2;
      if (top + menu.offsetHeight > viewportHeight) {
        top = buttonRect.top - menu.offsetHeight - 2;
      }

      menu.style.top = `${top}px`;
      menu.style.right = "0";
    }
  };

  useEffect(() => {
    if (isMenuOpen) {
      positionMenu();
      window.addEventListener("resize", positionMenu);
      return () => window.removeEventListener("resize", positionMenu);
    }
  }, [isMenuOpen]);

  return (
    <header className="flex items-center justify-between px-4 py-3 bg-gray-900 border-b border-gray-800 shadow-sm relative">
      <div className="flex items-center">
        <AiAvatar />
        <h1 className="ml-2 text-lg font-semibold text-white">LexiGPT</h1>
      </div>
      <div className="flex items-center space-x-2 relative">
        <button
          ref={profileButtonRef}
          onClick={handleProfileClick}
          className="flex items-center justify-center w-8 h-8 rounded-full overflow-hidden bg-gray-600 border border-gray-700 hover:border-gray-500 transition-all duration-200"
          aria-label="Profile menu"
          aria-expanded={isMenuOpen}
          aria-controls="profile-menu"
        >
          {userProfile?.picture ? (
            <img
              src={userProfile.picture}
              alt="User Profile"
              className="w-full h-full object-cover"
              onError={(e) => {
                (e.target as HTMLImageElement).src = "/default-avatar.jpg";
              }}
            />
          ) : (
            <span className="text-white text-sm">?</span>
          )}
        </button>
        {userProfile?.name && (
          <span
            onClick={handleProfileClick}
            className="ml-2 text-white font-medium text-sm cursor-pointer hover:text-gray-300 transition-colors duration-200"
          >
            {userProfile.name}
          </span>
        )}
        {isMenuOpen && (
          <div
            ref={menuRef}
            id="profile-menu"
            role="menu"
            className="absolute z-50 w-48 bg-gradient-to-b from-black via-gray-900 to-black border border-gray-700 rounded-xl shadow-lg animate-slide-down"
          >
            <ul className="py-1">
              <li>
                <button
                  role="menuitem"
                  onClick={handleDeleteUserData}
                  className="flex items-center w-full text-left px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors duration-200"
                >
                  <span className="mr-2 text-gray-400">🗑️</span> Clear User Data
                </button>
              </li>
              <li>
                <button
                  role="menuitem"
                  onClick={handleSignOut}
                  className="flex items-center w-full text-left px-4 py-2 text-gray-300 hover:bg-red-700 hover:text-white transition-colors duration-200"
                >
                  <span className="mr-2 text-gray-400">🚪</span> Sign Out
                </button>
              </li>
            </ul>
          </div>
        )}
      </div>
    </header>
  );
});

Header.displayName = "Header";
