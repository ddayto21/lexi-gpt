import React, { ElementType } from "react";
import Markdown from "markdown-to-jsx";

/**
 * Options for rendering markdown content using markdown-to-jsx.
 *
 * The `overrides` property allows us to specify custom rendering for specific
 * markdown elements. For example, we define custom components for headings,
 * lists, blockquotes, code blocks, etc., along with appropriate CSS classes
 * to match our UI design.
 *
 * @type {object}
 */
const markdownOptions = {
  overrides: {
    // Override rendering for h1 elements (Markdown headings)
    h1: {
      component: "h1" as ElementType,
      props: {
        className: "text-2xl font-bold mb-4",
      },
    },
    // Override rendering for h2 elements
    h2: {
      component: "h2" as ElementType,
      props: {
        className: "text-xl font-bold mb-3",
      },
    },
    // Override rendering for h3 elements
    h3: {
      component: "h3" as ElementType,
      props: {
        className: "text-lg font-bold mb-2",
      },
    },
    // Override rendering for unordered lists
    ul: {
      component: "ul" as ElementType,
      props: {
        className: "list-disc pl-5 mb-2",
      },
    },
    // Override rendering for ordered lists
    ol: {
      component: "ol" as ElementType,
      props: {
        className: "list-decimal pl-5 mb-2",
      },
    },
    // Override rendering for list items
    li: {
      component: "li" as ElementType,
      props: {
        className: "mb-1",
      },
    },
    // Override rendering for blockquotes
    blockquote: {
      component: "blockquote" as ElementType,
      props: {
        className: "border-l-4 pl-4 italic text-gray-600 my-4",
      },
    },
    // Override rendering for inline code
    code: {
      component: "code" as ElementType,
      props: {
        className: "bg-gray-200 rounded px-1 py-0.5",
      },
    },
    // Override rendering for code blocks
    pre: {
      component: "pre" as ElementType,
      props: {
        className: "bg-gray-800 text-white p-4 rounded my-2 overflow-x-auto",
      },
    },
  },
};

/**
 * ChatMarkdown component renders markdown content for chat messages.
 *
 * It uses markdown-to-jsx with custom options to transform markdown syntax into
 * React elements with specific styling for headings, lists, blockquotes, code blocks, etc.
 *
 * @param {object} props - Component properties.
 * @param {string} props.content - The markdown content to render.
 * @returns {JSX.Element} A React element that renders the formatted markdown.
 */
export const ChatMarkdown: React.FC<{ content: string }> = ({ content }) => {
  // Convert single newlines to "  \n" (two spaces before the newline).
  // This tells Markdown that each single newline is a line break.
  const forceLineBreaks = content.replace(/\n/g, "  \n");

  return <Markdown options={markdownOptions}>{forceLineBreaks}</Markdown>;
};
