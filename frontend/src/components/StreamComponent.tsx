// frontend/src/components/StreamComponent.tsx
import React, { useEffect, useState, useRef } from "react";
import { fetchEventSource } from "@microsoft/fetch-event-source";

interface Recommendation {
  title: string;
  description: string;
}

export function StreamComponent() {
  const [rawStream, setRawStream] = useState("");
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  // Clean an incoming chunk by removing markdown markers.
  const cleanChunk = (chunk: string): string => {
    let cleaned = chunk.trim();
    if (cleaned.startsWith("```json")) {
      cleaned = cleaned.slice(7).trim();
    }
    if (cleaned.endsWith("```")) {
      cleaned = cleaned.slice(0, -3).trim();
    }
    return cleaned;
  };

  useEffect(() => {
    let buffer = "";
    const fetchData = async () => {
      await fetchEventSource("http://localhost:8000/search_books", {
        method: "POST",
        body: JSON.stringify({ query: "anime similar to hunter x hunter" }),
        headers: { "Content-Type": "application/json" },
        onmessage(ev) {
          console.log(`Received event: ${ev.event}`);
          const cleaned = cleanChunk(ev.data);
          // If buffer doesn't end with space and cleaned chunk doesn't start with one, add a space.
          if (
            buffer &&
            cleaned &&
            !buffer.endsWith(" ") &&
            !cleaned.startsWith(" ")
          ) {
            buffer += " ";
          }
          buffer += cleaned;
          setRawStream(buffer);

          // Try to parse the accumulated buffer as JSON.
          try {
            const parsed = JSON.parse(buffer);
            if (Array.isArray(parsed)) {
              setRecommendations(parsed);
              // Once parsed successfully, clear the buffer.
              buffer = "";
              setRawStream("");
            }
          } catch (e) {
            // If parsing fails (incomplete JSON), continue buffering.
          }
        },
        onerror(err) {
          console.error("EventSource error:", err);
        },
      });
    };
    fetchData();
  }, []);

  // Auto-scroll to bottom when new text arrives.
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [rawStream, recommendations]);

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
      {recommendations.length > 0 ? (
        recommendations.map((rec, index) => (
          <div
            key={index}
            style={{
              marginBottom: "1rem",
              padding: "0.5rem",
              border: "1px solid #eee",
              borderRadius: "4px",
            }}
          >
            <h3 style={{ margin: "0 0 0.5rem 0" }}>{rec.title}</h3>
            <p style={{ margin: 0 }}>{rec.description}</p>
          </div>
        ))
      ) : (
        <p>{rawStream}</p>
      )}
    </div>
  );
}
