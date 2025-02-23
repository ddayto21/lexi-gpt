import React from "react";
import { Play, FileText } from "lucide-react";
import { Link } from "react-router-dom";

export function ActionButtons() {
  return (
    <div className="flex gap-4">
      {/* Start Demo Button */}
      <Link to="/login">
        <button className="flex items-center gap-2 px-6 py-2 border border-white/30 rounded-lg text-white bg-transparent hover:bg-white/10 transition-all">
          <Play className="w-5 h-5" />
          Start Demo
        </button>
      </Link>

      <Link to="https://github.com/ddayto21/lexi-gpt">
        <button className="px-6 py-2 bg-white text-black font-medium rounded-lg hover:bg-gray-200 transition-all">
          Documentation
        </button>
      </Link>
    </div>
  );
}
