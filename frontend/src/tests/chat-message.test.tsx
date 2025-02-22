/**
 * @jest-environment jsdom
 */
import React from "react";
import { render, } from "@testing-library/react";
import { ChatMessageComponent } from "../components/ui/chat/chat-message";
import type { Message as OriginalMessage } from "@ai-sdk/react";

interface Message extends OriginalMessage {
  timestamp: string;
}

describe("ChatMessageComponent", () => {
  it("renders assistant message with properly formatted markdown", () => {
    const message: Message = {
      role: "assistant",
      content: `
data: # Great choice! Historical fiction is a rich and diverse genre, full of suspense, twists, and heart-p ounding moments!
data: Here are some gripping thrill ers across different sub gen res to get you started:
data: ### Psychological Thr illers
data: 1."G one Girl"by Gill ian Flynn   - A dark, twist y tale of a marriage gone wrong, with unreliable narr ators and shocking revelations.
data: 2."The Silent Patient"by Alex Michael ides   - A psychological thriller about a woman who stops speaking after a shocking act of violence, and the therapist determined to uncover her secrets.
data: 3."Behind Closed Doors"by B. A. Paris   - A chilling story about a seemingly perfect couple with a horr ifying secret.
`,
      id: "msg-1",
      timestamp: new Date().toISOString(),
    };

    const { container } = render(<ChatMessageComponent msg={message} />);
    // Optionally, you can use a snapshot test:
    expect(container).toMatchSnapshot();

    // Or assert specific text (ensuring there are no double spaces in the rendered text)
    const renderedText = container.textContent || "";
    // Check that words like "thrillers" are correctly joined, e.g., no "thr illers"
    expect(renderedText).not.toMatch(/\b[a-zA-Z]+\s{2,}[a-zA-Z]+\b/);
  });
});
