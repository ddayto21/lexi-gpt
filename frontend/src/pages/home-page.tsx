import React, { useState, useEffect } from "react";
import { NavigationBar } from "@components/ui/navigation-bar";
import { ActionButtons } from "@components/ui/action-buttons";

import { Settings } from "lucide-react";
import { ChatMessageComponent } from "@components/ui/chat/chat-message";

export function HomePage() {
  const [showUserMessage, setShowUserMessage] = useState(false);
  const [showAIResponse, setShowAIResponse] = useState(false);

  useEffect(() => {
    const timer1 = setTimeout(() => setShowUserMessage(true), 2000);
    const timer2 = setTimeout(() => setShowAIResponse(true), 4000);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, []);

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white overflow-hidden">
      <NavigationBar />

      {/* Hero Section */}
      <section className="py-16 px-6">
        <div className="container mx-auto max-w-7xl">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="text-left space-y-8">
              <h1 className="text-5xl lg:text-7xl font-bold leading-tight animate-fade-in-up">
                Your AI-Powered{" "}
                <span className="bg-gradient-to-r from-blue-500 to-purple-600 text-transparent bg-clip-text">
                  Reading Assistant
                </span>
              </h1>
              <p className="text-xl text-gray-400 max-w-2xl animate-fade-in-up animation-delay-300">
                Engage in natural conversations to discover books tailored to
                your taste. LexiGPT learns your reading preferences and provides
                **insightful recommendations, summaries, and analysis**—all in
                real-time.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 animate-fade-in-up animation-delay-600">
                <ActionButtons />
              </div>
            </div>

            {/* Chat UI - Using ChatMessageComponent */}
            <div className="relative animate-float">
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
                  <ChatMessageComponent
                    msg={{
                      id: "1",
                      role: "assistant",
                      content:
                        "Hello! I'm LexiGPT, your AI reading assistant. What book are you in the mood for today?",
                      timestamp: new Date().toISOString(),
                    }}
                  />
                  {showUserMessage && (
                    <ChatMessageComponent
                      msg={{
                        id: "2",
                        role: "user",
                        content:
                          "I'm looking for a thought-provoking sci-fi book. Any recommendations?",
                        timestamp: new Date().toISOString(),
                      }}
                    />
                  )}
                  {showAIResponse && (
                    <ChatMessageComponent
                      msg={{
                        id: "3",
                        role: "assistant",
                        content:
                          "I'd recommend *The Three-Body Problem* by Liu Cixin—an epic sci-fi masterpiece exploring first contact and survival on a cosmic scale. Would you like a quick summary?",
                        timestamp: new Date().toISOString(),
                      }}
                    />
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
