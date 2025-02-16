// src/components/StreamComponent.tsx
import React, { useEffect, useState, useRef } from "react";
import { fetchEventSource } from "@microsoft/fetch-event-source";

interface Recommendation {
  title: string;
  description: string;
}

interface StreamComponentProps {
  query: string;
}

export function StreamComponent({ query }: StreamComponentProps) {
  const [rawStream, setRawStream] = useState("");
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  // Remove markdown markers and extra whitespace.
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
        body: JSON.stringify({ query }),
        headers: { "Content-Type": "application/json" },
        onmessage(ev) {
          console.log(`Received event: ${ev.event}`);
          const cleaned = cleanChunk(ev.data);
          // Insert space if needed.
          if (
            buffer &&
            !buffer.endsWith(" ") &&
            cleaned &&
            !cleaned.startsWith(" ")
          ) {
            buffer += " ";
          }
          buffer += cleaned;
          setRawStream(buffer);

          // Try parsing JSON.
          try {
            const parsed = JSON.parse(buffer);
            if (Array.isArray(parsed)) {
              setRecommendations(parsed);
              buffer = "";
              setRawStream("");
            }
          } catch (e) {
            // Incomplete JSON, continue buffering.
          }
        },
        onerror(err) {
          console.error("EventSource error:", err);
        },
      });
    };
    fetchData();
  }, [query]);

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
        backgroundColor: "#343541",
        color: "#ffffff",
        border: "1px solid #555",
        padding: "1rem",
      }}
    >
      {recommendations.length > 0 ? (
        recommendations.map((rec, index) => (
          <div
            key={index}
            style={{
              marginBottom: "1rem",
              padding: "1rem",
              backgroundColor: "#202123",
              borderRadius: "8px",
              boxShadow: "0 2px 4px rgba(0,0,0,0.5)",
            }}
          >
            <h3 style={{ margin: "0 0 0.5rem 0", color: "#ffffff" }}>
              {rec.title}
            </h3>
            <p style={{ margin: 0, color: "#c9c9c9" }}>{rec.description}</p>
          </div>
        ))
      ) : (
        <p>{rawStream}</p>
      )}
    </div>
  );
}
