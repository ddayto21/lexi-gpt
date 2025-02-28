import React, { useState, useEffect } from "react";
import { AiAvatar } from "@components/ui/avatars/ai-avatar";

export const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [userProfile, setUserProfile] = useState<{
    picture?: string;
    name?: string;
  } | null>(null);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const response = await fetch("/api/auth/profile", {
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
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

  const handleProfileClick = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleSignOut = async () => {
    try {
      const response = await fetch("http://localhost:8000/auth/signout", {
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

  return (
    <header className="flex items-center justify-between px-4 py-3 bg-neutral-900 border-b border-neutral-800 shadow-md relative">
      <div className="flex items-center">
        <AiAvatar />
        <h1 className="ml-2 text-lg font-bold text-white">AI Book Finder</h1>
      </div>
      <div className="flex items-center space-x-2 relative">
        <button className="text-gray-400 hover:text-gray-300">
          <svg
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </button>
        <button className="text-gray-400 hover:text-gray-300">
          <svg
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37a1.724 1.724 0 002.572-1.065z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
        </button>
        <div className="relative">
          <button
            onClick={handleProfileClick}
            className="flex items-center justify-center w-8 h-8 rounded-full overflow-hidden bg-gray-500"
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
              <span className="text-white">?</span>
            )}
          </button>
          {isMenuOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-neutral-800 border border-neutral-700 rounded-md shadow-lg z-10">
              <ul className="py-1">
                <li>
                  <button className="block w-full text-left px-4 py-2 text-gray-300 hover:bg-neutral-700 hover:text-white">
                    Settings
                  </button>
                </li>
                <li>
                  <button className="block w-full text-left px-4 py-2 text-gray-300 hover:bg-neutral-700 hover:text-white">
                    Help & Feedback
                  </button>
                </li>
                <li>
                  <button
                    onClick={handleSignOut}
                    className="block w-full text-left px-4 py-2 text-gray-300 hover:bg-neutral-700 hover:text-white"
                  >
                    Sign Out
                  </button>
                </li>
              </ul>
            </div>
          )}
        </div>
        {userProfile && userProfile.name && (
          <span className="ml-2 text-white font-medium">
            {userProfile.name}
          </span>
        )}
      </div>
    </header>
  );
};
