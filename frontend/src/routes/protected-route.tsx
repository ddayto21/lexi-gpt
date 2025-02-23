import React from "react";
import { Navigate } from "react-router-dom";

export function ProtectedRoute({ children }: { children: React.JSX.Element }) {
  const token = localStorage.getItem("token");

  return token ? children : <Navigate to="/login" />;
}
