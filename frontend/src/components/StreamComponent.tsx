// frontend/src/components/StreamComponent.tsx
import React, { useEffect } from "react";
import { fetchEventSource } from "@microsoft/fetch-event-source";

interface StreamComponentProps {
  query: string;
  onStreamUpdate: (partialText: string) => void;
  onStreamComplete: () => void;
}

export function StreamComponent({
  query,
  onStreamUpdate,
  onStreamComplete,
}: StreamComponentProps) {
  useEffect(() => {
    let buffer = "";
    let streamFinished = false; // Prevent further processing after DONE marker.
    const fetchData = async () => {
      await fetchEventSource("http://localhost:8000/search_books", {
        method: "POST",
        body: JSON.stringify({ query }),
        headers: { "Content-Type": "application/json" },
        onmessage(ev) {
          // If the stream is already finished, ignore further messages.
          if (streamFinished) return;

          let chunk = ev.data.trim();

          // Check if the chunk is exactly "[DONE]" or contains it.
          if (chunk === "[DONE]") {
            streamFinished = true;
            onStreamComplete();
            return;
          } else if (chunk.includes("[DONE]")) {
            // Remove the marker from the chunk.
            chunk = chunk.replace("[DONE]", "").trim();
            streamFinished = true;
            // Append the cleaned chunk to the buffer.
            if (
              buffer &&
              !buffer.endsWith(" ") &&
              chunk &&
              !chunk.startsWith(" ")
            ) {
              buffer += " ";
            }
            buffer += chunk;
            onStreamUpdate(buffer);
            onStreamComplete();
            return;
          }

          // Insert a space between chunks if needed.
          if (
            buffer &&
            !buffer.endsWith(" ") &&
            chunk &&
            !chunk.startsWith(" ")
          ) {
            buffer += " ";
          }
          buffer += chunk;
          onStreamUpdate(buffer);
        },
        onerror(err) {
          console.error("EventSource error:", err);
          onStreamComplete();
        },
      });
    };
    fetchData();

    // Cleanup on unmount.
    return () => {
      onStreamComplete();
    };
  }, [query, onStreamUpdate, onStreamComplete]);

  return null;
}
