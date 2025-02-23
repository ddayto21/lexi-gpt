import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import { HomePage } from "@pages/home-page";
import { ChatPage } from "@pages/chat-page";
import { LoginPage } from "@pages/login-page";

import { ProtectedRoute } from "@routes/protected-route";
export function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <ChatPage />

            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" />} />{" "}
      </Routes>
    </Router>
  );
}
