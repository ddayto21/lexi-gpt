import type React from "react"
import { LightAsync as SyntaxHighlighter } from "react-syntax-highlighter"
import { atomOneDark } from "react-syntax-highlighter/dist/esm/styles/hljs"

interface CodeDemoProps {
  title: string
  code: string
}

export const CodeDemo: React.FC<CodeDemoProps> = ({ title, code }) => {
  return (
    <div className="bg-gray-900 rounded-xl overflow-hidden shadow-lg">
      <div className="flex items-center justify-between px-4 py-2 bg-gray-800">
        <h3 className="text-sm font-semibold text-gray-300">{title}</h3>
        <div className="flex space-x-2">
          <div className="w-3 h-3 rounded-full bg-red-500"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
          <div className="w-3 h-3 rounded-full bg-green-500"></div>
        </div>
      </div>
      <SyntaxHighlighter
        language="python"
        style={atomOneDark}
        customStyle={{
          padding: "1rem",
          fontSize: "0.875rem",
          lineHeight: "1.5",
          margin: 0,
        }}
      >
        {code.trim()}
      </SyntaxHighlighter>
    </div>
  )
}