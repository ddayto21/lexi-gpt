import React, { ElementType } from "react";
import Markdown from "markdown-to-jsx";

import hljs from "highlight.js";
import "highlight.js/styles/github-dark.css";

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
    h1: {
      component: "h1" as ElementType,
      props: {
        className: "text-3xl font-bold mb-4 text-white",
      },
    },
    h2: {
      component: "h2" as ElementType,
      props: {
        className: "text-2xl font-bold mb-3 text-white",
      },
    },
    h3: {
      component: "h3" as ElementType,
      props: {
        className: "text-xl font-bold mb-2 text-white",
      },
    },
    ul: {
      component: "ul" as ElementType,
      props: {
        className: "list-disc pl-6 mb-2 text-gray-300",
      },
    },
    ol: {
      component: "ol" as ElementType,
      props: {
        className: "list-decimal pl-6 mb-2 text-gray-300",
      },
    },
    li: {
      component: "li" as ElementType,
      props: {
        className: "mb-1",
      },
    },
    blockquote: {
      component: "blockquote" as ElementType,
      props: {
        className: "border-l-4 pl-4 italic text-gray-400 my-4 text-gray-300",
      },
    },
    code: {
      component: "code" as ElementType,
      props: {
        className: "bg-gray-700 rounded px-1 py-0.5 text-gray-100",
      },
    },
    pre: {
      component: "pre" as ElementType,
      props: {
        className: "bg-gray-800 text-white p-4 rounded my-2 overflow-x-auto",
      },
      children: (props: { children: React.ReactNode }) => {
        const code = Array.isArray(props.children)
          ? props.children.join("")
          : props.children;
        const highlightedCode = hljs.highlightAuto(code as string).value;
        return <code className="hljs">{highlightedCode}</code>;
      },
    },
    p: {
      component: "p" as ElementType,
      props: {
        className: "mb-2 text-gray-300",
      },
    },
    a: {
      component: "a" as ElementType,
      props: {
        className: "text-blue-400 hover:text-blue-500",
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
