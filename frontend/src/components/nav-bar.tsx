import React from "react";
import { Link } from "react-router-dom";

export function Navbar() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/chat">Chat</Link>
      <Link to="/login">Login</Link>
    </nav>
  );
}
