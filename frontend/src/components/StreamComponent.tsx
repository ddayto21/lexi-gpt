// frontend/src/components/StreamComponent.tsx
import React, { useEffect, useState, useRef } from "react";
import { fetchEventSource } from "@microsoft/fetch-event-source";

export function StreamComponent() {
  const [streamText, setStreamText] = useState("");
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchData = async () => {
      await fetchEventSource("http://localhost:8000/search_books", {
        method: "POST",
        body: JSON.stringify({ query: "anime similar to hunter x hunter" }),
        headers: {
          "Content-Type": "application/json",
        },
        onmessage(ev) {
          console.log(`Received event: ${ev.event}`);
          setStreamText((prev) => prev + ev.data);
        },
        onerror(err) {
          console.error("EventSource failed:", err);
        },
      });
    };
    fetchData();
  }, []);

  // Auto-scroll to bottom as new text is appended.
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [streamText]);

  return (
    <div
      ref={containerRef}
      style={{
        height: "400px",
        overflowY: "auto",
        whiteSpace: "pre-wrap",
        fontFamily: "monospace",
        border: "1px solid #ccc",
        padding: "1rem",
      }}
    >
      {streamText}
    </div>
  );
}
