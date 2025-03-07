import React from "react";
import { FcGoogle } from "react-icons/fc";
import { Link } from "react-router-dom";
import { RAGProcess } from "@components/ui/features/rag-system";

// Ensure required environment variables are set
if (!process.env.REACT_APP_GOOGLE_CLIENT_ID) {
  throw new Error("REACT_APP_GOOGLE_CLIENT_ID is not set");
}

if (!process.env.REACT_APP_REDIRECT_URI) {
  throw new Error("REACT_APP_REDIRECT_URI is not set");
}

if (!process.env.REACT_APP_BASE_URL) {
  throw new Error("REACT_APP_BASE_URL is not set");
}

const BASE_API_URL = process.env.REACT_APP_BASE_URL;

export function LoginPage() {
  const handleLogin = () => {
    const CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID;
    // Your redirect URI should point to your backend /auth/callback endpoint
    const REDIRECT_URI = encodeURIComponent(`${BASE_API_URL}/auth/callback`);
    console.log(`Redirect URI: ${REDIRECT_URI}`);
    const SCOPE = encodeURIComponent("openid email profile");
    const PROMPT = "select_account"; // Forces Google to always prompt for account selection

    const authUrl =
      `https://accounts.google.com/o/oauth2/v2/auth?` +
      `client_id=${CLIENT_ID}` +
      `&redirect_uri=${REDIRECT_URI}` +
      `&response_type=code` +
      `&scope=${SCOPE}` +
      `&access_type=offline` +
      `&prompt=${PROMPT}`;

    // window.location.href = authUrl;

    // Full-page redirect
    window.open(authUrl);
  };

  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-[#0a0a0a] text-white">
      {/* Left Side: Markdown Demo */}
      <div className="hidden lg:flex flex-col items-center justify-center p-8 bg-gradient-to-b from-blue-900 to-purple-900 text-white">
        <div className="w-full max-w-lg mx-auto space-y-12">
          <div className="w-[450px]">
            <RAGProcess />
          </div>
        </div>
      </div>

      {/* Right Side: Login Form */}
      <div className="flex flex-col items-center justify-center p-8">
        <div className="w-full max-w-sm space-y-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 text-transparent bg-clip-text">
              LexiGPT
            </h1>
            <h2 className="text-xl text-gray-300 mt-2">Welcome Back</h2>
          </div>

          <form className="space-y-6">
            {/* Google Sign-In Button */}
            <button
              onClick={() => handleLogin()}
              className="flex items-center justify-center w-full p-3 rounded-full bg-white text-black font-medium text-lg transition hover:bg-gray-200"
            >
              <FcGoogle className="mr-2 text-2xl" />
              Log in with Google
            </button>

            {/* Divider */}
            <div className="relative text-center">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-700"></div>
              </div>
              <div className="relative inline-block px-2 bg-[#0a0a0a] text-gray-400">
                or
              </div>
            </div>

            <p className="text-center text-sm text-gray-400">
              Don&apos;t have an account?{" "}
              <Link to="/signup" className="text-blue-500 hover:underline">
                Sign Up
              </Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
