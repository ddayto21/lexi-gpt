import React, { useState, useEffect, useRef } from "react";
import { AiAvatar } from "@components/ui/avatars/ai-avatar";

const API_BASE_URL = process.env.REACT_APP_BASE_URL;
if (!API_BASE_URL) {
  throw new Error("API_BASE_URL is not set");
}

export const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [userProfile, setUserProfile] = useState<{
    picture?: string;
    name?: string;
  } | null>(null);
  const menuRef = useRef<HTMLDivElement>(null); // Ref for the menu
  const profileButtonRef = useRef<HTMLButtonElement>(null); // Ref for the profile button

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/auth/profile`, {
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
          console.log(`User profile data:`, JSON.stringify(data, null, 2));
          setUserProfile(data.profile || data.user);
        } else {
          console.error("Failed to fetch profile:", response.statusText);
        }
      } catch (error) {
        console.error("Failed to fetch user profile:", error);
      }
    };

    fetchUserProfile();
  }, []);

  const handleProfileClick = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsMenuOpen(!isMenuOpen);
  };

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

  // New function: Send DELETE request to clear user data from cache.
  const handleDeleteUserData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/cache`, {
        method: "DELETE",
        credentials: "include",
      });
      if (response.ok) {
        console.log("User data deleted from cache.");
        // Optionally, update UI state or provide user feedback.
      } else {
        console.error("Failed to delete user data:", response.statusText);
      }
    } catch (error) {
      console.error("Error deleting user data:", error);
    }
    setIsMenuOpen(false);
  };

  // Close menu when clicking outside
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
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isMenuOpen]);

  // Dynamically position the menu to stay within viewport
  const positionMenu = () => {
    if (menuRef.current && profileButtonRef.current) {
      const buttonRect = profileButtonRef.current.getBoundingClientRect();
      const menu = menuRef.current;
      const viewportHeight = window.innerHeight;

      let top = buttonRect.bottom + 2; // Default margin-top of 2px
      if (top + menu.offsetHeight > viewportHeight) {
        top = buttonRect.top - menu.offsetHeight - 2; // Position above if it would exceed viewport
      }

      menu.style.top = `${top}px`;
      menu.style.right = "0";
    }
  };

  useEffect(() => {
    if (isMenuOpen && menuRef.current && profileButtonRef.current) {
      positionMenu();
      window.addEventListener("resize", positionMenu);
    }
    return () => window.removeEventListener("resize", positionMenu);
  }, [isMenuOpen]);

  return (
    <header className="flex items-center justify-between px-4 py-3 bg-gray-900 border-b border-gray-800 shadow-sm relative">
      <div className="flex items-center">
        <AiAvatar />
        <h1 className="ml-2 text-lg font-semibold text-white">LexiGPT</h1>
      </div>
      <div className="flex items-center space-x-2 relative">
        <button
          ref={profileButtonRef} // Attach ref to profile button
          onClick={handleProfileClick}
          className="profile-button flex items-center justify-center w-8 h-8 rounded-full overflow-hidden bg-gray-600 border border-gray-700 hover:border-gray-500 transition-all duration-200"
          aria-label="Profile menu"
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
        {userProfile && userProfile.name && (
          <span
            onClick={handleProfileClick}
            className="ml-2 text-white font-medium text-sm cursor-pointer hover:text-gray-300 transition-colors duration-200"
          >
            {userProfile.name}
          </span>
        )}
        {isMenuOpen && (
          <div
            ref={menuRef} // Attach ref to menu
            className="header-menu absolute z-50 w-48 bg-gradient-to-b from-black via-gray-900 to-black border border-gray-700 rounded-xl shadow-lg animate-slide-down"
          >
            <ul className="py-1">
              <li>
                <button
                  onClick={handleDeleteUserData}
                  className="flex items-center w-full text-left px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors duration-200"
                >
                  <span className="mr-2 text-gray-400">🗑️</span> Clear User Data
                </button>
              </li>

              <li>
                <button
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
};
