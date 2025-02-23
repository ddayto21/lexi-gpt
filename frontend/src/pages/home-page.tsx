import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@components/button";
import { ArrowRight, Zap, Book, Settings } from "lucide-react";

export function HomePage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Navigation */}
      <nav className="border-b border-gray-800 backdrop-blur-md">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Zap className="w-8 h-8 text-blue-500" />
            <span className="text-xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 text-transparent bg-clip-text">
              LexiGPT
            </span>
          </div>
          <div className="hidden md:flex items-center gap-6">
            <Link to="#" className="text-gray-400 hover:text-white transition">
              Features
            </Link>
            <Link to="#" className="text-gray-400 hover:text-white transition">
              Pricing
            </Link>
            <Link to="#" className="text-gray-400 hover:text-white transition">
              About
            </Link>
            <Button
              variant="outline"
              className="border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white"
            >
              Sign In
            </Button>
            <Button className="bg-blue-500 hover:bg-blue-600">
              Get Started
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-7xl">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="text-left space-y-8">
              <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                Your AI-Powered{" "}
                <span className="bg-gradient-to-r from-blue-500 to-purple-600 text-transparent bg-clip-text">
                  Reading Assistant
                </span>
              </h1>
              <p className="text-xl text-gray-400 max-w-2xl">
                Experience a smarter way to discover books. LexiGPT uses
                advanced AI to understand your reading preferences, provide
                tailored recommendations, and offer insightful book
                summaries—all through a natural conversation.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  size="lg"
                  className="bg-blue-500 hover:bg-blue-600 text-lg px-8 py-4"
                >
                  Start Exploring <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="text-white border-gray-700 hover:bg-gray-800 text-lg px-8 py-4"
                >
                  How It Works <Book className="ml-2 h-5 w-5" />
                </Button>
              </div>
            </div>

            {/* Chat UI */}
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-600/10 rounded-3xl filter blur-3xl"></div>
              <div className="relative bg-gray-900 rounded-3xl p-8 shadow-2xl border border-gray-800">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  </div>
                  <Settings className="text-gray-500 w-5 h-5" />
                </div>
                <div className="space-y-4">
                  <div className="bg-blue-500 text-white p-3 rounded-2xl rounded-bl-none max-w-[80%]">
                    Hello! I'm LexiGPT, your AI reading assistant. What book are
                    you in the mood for today?
                  </div>
                  <div className="bg-gray-800 text-white p-3 rounded-2xl rounded-br-none max-w-[80%] ml-auto">
                    I'm looking for a thought-provoking sci-fi book. Any
                    recommendations?
                  </div>
                  <div className="bg-blue-500 text-white p-3 rounded-2xl rounded-bl-none max-w-[80%]">
                    I’d recommend *The Three-Body Problem* by Liu Cixin—an epic
                    sci-fi masterpiece exploring first contact and survival on a
                    cosmic scale. Would you like a quick summary?
                  </div>
                </div>
                <div className="mt-6 flex items-center bg-gray-800 rounded-full p-2">
                  <input
                    type="text"
                    placeholder="Ask LexiGPT..."
                    className="flex-grow bg-transparent outline-none text-white placeholder-gray-500 px-3"
                  />
                  <Button
                    size="sm"
                    className="bg-blue-500 hover:bg-blue-600 rounded-full p-2"
                  >
                    <ArrowRight className="h-5 w-5" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
