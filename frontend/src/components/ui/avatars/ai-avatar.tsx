import React from "react";

interface AiAvatarProps {
  size?: "sm" | "md" | "lg";
}

export const AiAvatar: React.FC<AiAvatarProps> = ({ size = "md" }) => {
  const sizeClasses = {
    sm: "h-6 w-6",
    md: "h-8 w-8",
    lg: "h-10 w-10",
  };

  return (
    <div className="flex-none mr-2">
      <div
        className={`${sizeClasses[size]} rounded-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center`}
      >
        <svg
          className="w-2/3 h-2/3 text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 4v1m6.364 1.636l-.707.707M20 12h-1M17.657 17.657l-.707-.707M12 20v-1m-6.364-1.636l.707-.707M4 12h1m2.343-5.657l.707.707M12 4a8 8 0 100 16 8 8 0 000-16z"
          />
        </svg>
      </div>
    </div>
  );
};
