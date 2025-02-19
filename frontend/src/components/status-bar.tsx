import React from "react";

interface StatusBarProps {
  status: string;
  errorMessage?: string | null;
}

export const StatusBar: React.FC<StatusBarProps> = ({ status, errorMessage }) => (
  <div className="px-4 py-2 border-b border-neutral-800 bg-black">
    <p className="text-sm text-gray-300">Status: {status}</p>
    {errorMessage && (
      <div className="mt-2 p-2 bg-red-600 text-white rounded-md">
        Error: {errorMessage}
      </div>
    )}
  </div>
);


