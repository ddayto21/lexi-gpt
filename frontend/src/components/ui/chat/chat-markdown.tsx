import React from "react";
import Markdown from "markdown-to-jsx";

/**
 * ChatMarkdown component renders markdown content for chat messages.
 * It uses markdown-to-jsx to parse markdown and convert it into React elements,
 * supporting common markdown features like bullet lists, headings, and code blocks.
 *
 * @param {object} props - Component properties.
 * @param {string} props.content - The markdown content to render.
 * @returns {JSX.Element} A React element that renders the markdown.
 */
export const ChatMarkdown: React.FC<{ content: string }> = ({ content }) => {
  return <Markdown>{content}</Markdown>;
};