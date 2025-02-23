import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@components/button";

import { ArrowRight, Zap } from "lucide-react";

export const NavigationBar = () => {
  return (
    <nav className="border-b border-gray-800 backdrop-blur-md sticky top-0 z-20">
      <div className="container mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/home">
          <div className="flex items-center gap-2">
            <Zap className="w-8 h-8 text-blue-500 animate-pulse" />
            <span className="text-xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 text-transparent bg-clip-text">
              LexiGPT
            </span>
          </div>
        </Link>
        <div className="hidden md:flex items-center gap-6">
          <Link to="/login">
            <Button
              variant="outline"
              className="relative flex items-center gap-3 px-6 py-2 border border-gray-700 text-gray-300 hover:text-white 
               bg-transparent rounded-lg transition-all duration-300 hover:bg-gray-800 hover:border-gray-600 
               shadow-md hover:shadow-lg transform hover:scale-105"
            >
              <span className="text-base font-medium">Sign In</span>
              <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-white transition-all" />
            </Button>
          </Link>
        </div>
      </div>
    </nav>
  );
};
