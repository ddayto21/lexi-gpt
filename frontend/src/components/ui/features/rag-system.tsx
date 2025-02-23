import React, { useState, useEffect } from "react";
import { Search, Database, ArrowRight, Book } from "lucide-react";
import { CodeDemo } from "./code-demo";

export const RAGProcess = () => {
  const [step, setStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setStep((prevStep) => (prevStep + 1) % steps.length);
    }, 6000);
    return () => clearInterval(timer);
  }, []);

  const steps = [
    {
      icon: <Search className="w-8 h-8" />,
      text: "Create Vector Embeddings",
      code: `
def create_vector_embedding():
    with torch.no_grad():
        embedding = model.encode([processed_text])
    return embedding
`,
    },
    {
      icon: <Database className="w-8 h-8" />,
      text: "Semantic Search",
      code: `
def semantic_search():
    query_embedding = create_vector_embedding(model, query)
    similarities = cosine_similarity(query_embedding, book_embeddings)
    top_indices = np.argsort(similarities[0])[::-1][:top_k]
    return top_indices.tolist()
`,
    },
    {
      icon: <ArrowRight className="w-8 h-8" />,
      text: "Augment Prompt",
      code: `
def augment_prompt():
    prompt = f"User Query: {query}\\n
        Context: {retrieved_docs}
    return augmented_prompt
`,
    },
    {
      icon: <Book className="w-8 h-8" />,
      text: "Generate Response",
      code: `
def generate_response():
    response = llm_model.generate(prompt)
    return response
`,
    },
  ];

  return (
    <div className="max-w-1xl mx-auto p-8 bg-gray-900 text-white rounded-xl shadow-lg">
      {/* Step Indicator UI */}
      <div className="flex justify-between items-center w-full py-4 border-b border-gray-700">
        {steps.map((s, index) => (
          <div
            key={index}
            className={`relative flex flex-col items-center transition-all duration-300 ${
              index === step ? "text-blue-500" : "text-gray-500"
            }`}
          >
            <div
              className={`w-12 h-12 flex items-center justify-center rounded-full border-2 ${
                index === step
                  ? "border-blue-500 bg-blue-900/30"
                  : "border-gray-600"
              }`}
            >
              {s.icon}
            </div>
            <span className="text-xs mt-2 text-center">{s.text}</span>
            {index !== steps.length - 1 && (
              <div className="absolute top-5 left-14 w-16 h-0.5 bg-gray-600"></div>
            )}
          </div>
        ))}
      </div>

      {/* Step Content (Fixed Height to Prevent Layout Shifting) */}
      <div className="mt-6 min-h-[300px] flex items-center justify-center mx-5">
        {steps.map((s, index) => (
          <div
            key={index}
            className={`transition-opacity duration-500 ease-in-out ${
              index === step ? "opacity-100 block" : "opacity-0 hidden"
            }`}
          >
            <CodeDemo title={s.text} code={s.code} />
          </div>
        ))}
      </div>
    </div>
  );
};
