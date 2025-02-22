/**
 * @jest-environment jsdom
 *
 * This test file verifies that the ChatMarkdown component correctly renders
 * markdown content. We use React Testing Library to render the component and Jest
 * to perform assertions. The tests cover:
 * - A snapshot test to capture the overall rendered output.
 * - Verifying that a markdown heading is rendered as a heading.
 * - Checking that bullet lists are rendered as list items.
 * - Ensuring that bold markdown is rendered as bold text.
 * - Confirming that blockquotes are rendered correctly.
 */

import React from "react";
import { render, screen } from "@testing-library/react";
import { ChatMarkdown } from "../components/ui/chat/chat-markdown"; // Adjust the import path as needed

describe("ChatMarkdown component", () => {
  /**
   * Snapshot Test:
   * This test renders the ChatMarkdown component with a sample markdown string containing
   * a heading, bullet list, bold text, and a blockquote. The resulting DOM output is saved
   * as a snapshot. Future changes to the output will cause this test to fail, alerting us to
   * unintended changes in the component's rendering.
   */
  it("renders markdown content correctly (snapshot)", () => {
    const markdownContent = `
# Heading 1

- Bullet 1
- Bullet 2

**Bold Text**

> A blockquote
    `;
    const { container } = render(<ChatMarkdown content={markdownContent} />);
    expect(container).toMatchSnapshot();
  });

  /**
   * Heading Test:
   * This test checks that a markdown heading is rendered correctly.
   * It passes a simple markdown string with a level 1 heading and then uses
   * getByRole to find the heading element. It asserts that the heading displays
   * the correct text.
   */
  it("renders a heading correctly", () => {
    const markdownContent = "# Heading Test";
    render(<ChatMarkdown content={markdownContent} />);
    const heading = screen.getByRole("heading", { level: 1 });
    expect(heading).toHaveTextContent("Heading Test");
  });

  /**
   * Bullet List Test:
   * This test verifies that a markdown bullet list is rendered as an unordered list
   * with list items. It renders markdown with two bullet points and then asserts that
   * exactly two list items are found, and that they contain the expected text.
   */
  it("renders a bullet list correctly", () => {
    const markdownContent = `
- Item 1
- Item 2
    `;
    render(<ChatMarkdown content={markdownContent} />);
    const listItems = screen.getAllByRole("listitem");
    expect(listItems.length).toBe(2);
    expect(listItems[0]).toHaveTextContent("Item 1");
    expect(listItems[1]).toHaveTextContent("Item 2");
  });

  /**
   * Bold Text Test:
   * This test ensures that text marked as bold in the markdown (using ** markers)
   * is rendered as bold. Bold text is usually rendered in a <strong> or <b> tag,
   * so we verify that the text is rendered in one of these tags.
   */
  it("renders bold text correctly", () => {
    const markdownContent = "**Bold Test**";
    render(<ChatMarkdown content={markdownContent} />);
    // Bold text is typically rendered as <strong> or <b>
    const boldElement = screen.getByText("Bold Test");
    expect(boldElement.tagName).toMatch(/^(STRONG|B)$/);
  });

  /**
   * Blockquote Test:
   * This test verifies that a markdown blockquote is rendered correctly.
   * It renders a simple blockquote and then uses DOM traversal to confirm that the
   * blockquote element exists in the document.
   */
  it("renders a blockquote correctly", () => {
    const markdownContent = "> This is a blockquote";
    render(<ChatMarkdown content={markdownContent} />);
    const blockquote = screen.getByText("This is a blockquote");
    // Ensure that the blockquote element is present in the document.
    expect(blockquote.closest("blockquote")).toBeInTheDocument();
  });
});