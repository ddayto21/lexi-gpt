# RAG System Overview

This RAG framework combines two steps to provide a recommendation for a book:

1. Retrieval: Find useful, relevant information (e.g., a list of books) based on the user’s query.

2. Generation: Use a language model (LLM) to create a helpful response using that information.

---

## RAG Workflow

### 1. **Retrieval Phase**

The retrieval component processes user queries to find relevant books using semantic similarity. It leverages embeddings to understand the meaning behind the query and retrieves the most relevant books.

#### Example Input

The user provides a search query for a particular book.

```json
{
  "query": "I am looking for anime book similar to hunter x hunter and death note"
}
```

#### Example Output

The retriever component searches for relevant documents from the knowledge base, and returns a list of 5 books that best match the query (each with title, author, subjects, year, book_id).

```json
[
  {
    "book_id": "OL3946622W",
    "title": "gorin sho",
    "author": "miyamoto musashi",
    "subjects": "biography, bushido, ciencia militar, early work, kendo, management, martial art, military art science, military science ... ...",
    "year": "1963",
    "embedding_input": "Title: gorin sho. Author: miyamoto musashi. Subjects: biography, bushido, ciencia, ... Year: 1963."
  }
]
```

---

### 2. Generation Phase

- Prompt Construction: The system builds a prompt that includes the retrieved book details. For example, it might list each book’s title, author, year, and key subjects.

- Response Generation: The prompt is sent to an LLM to generate a JSON array of book recommendations.

Each recommendation includes:

- title: name of the book
- description: an explanation of why the book is relevant to the user’s query.

If the retrieved books don’t seem to match the query well, the model can provide its own recommendations based on internal knowledge.

---

#### Example Input (LLM Prompt)

```python

User query: 'I am looking for anime books similar to hunter x hunter and death note'.

RAG system has retrieved relevant book details:

1. Hunter x Hunter by Yoshihiro Togashi (1998). Keywords: magic, hunter, graphic novel
2. Inuyasha by Rumiko Takahashi (1998). Keywords: action, supernatural, adventure
3. Wood Queen Iron Witch Trilogy Book by Karen Mahoney (2012). Keywords: fantasy, paranormal, romance
4. Berenstain Bear Activity Book by Stan Berenstain (1991). Keywords: family, classic, children
5. Demon Seed by Dean Koontz (1973). Keywords: horror, thriller, artificial intelligence

Based on these details, provide a JSON array of book recommendations. Each recommendation should be an object with a 'title' and a 'description' that explains in clear, friendly language why the book is relevant to the query. If none of the retrieved books match the query, please generate your own recommendations based on your internal knowledge. Return only the JSON array.


```

#### Example Output (LLM Response)

```json
[
  {
    "title": "Hunter x Hunter by Yoshihiro Togashi",
    "description": "This book is perfect because it has complex strategies and epic battles, just like what you love about Hunter x Hunter."
  },
  {
    "title": "Inuyasha by Rumiko Takahashi",
    "description": "Inuyasha blends action with supernatural themes, offering a similar adventurous spirit."
  },
  {
    "title": "Fullmetal Alchemist by Hiromu Arakawa",
    "description": "Known for its deep storyline and moral dilemmas, this series offers rich characters and exciting battles."
  }
]
```

---

## Testing

To test the RAG system, you can send a POST request to the /search_books endpoint. For example, using curl:

```bash

curl -L -X POST 'http://localhost:8000/api/chat/stream' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer sk-0b9228bcb36c47058dc740696a9ddd1a' \
--data-raw '{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant that provides clear and accurate book recommendations and explanations. Respond in a friendly, concise, and professional manner."
    },
    {
      "role": "user",
      "content": "Provide book recommendations that are similar to Code Geass."
    }
  ],
  "model": "deepseek-chat",
  "max_tokens": 500,
  "response_format": "text",
  "stream": true,
  "temperature": 1
}'

```

```bash
curl -L -X POST 'https://api.deepseek.com/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer sk-0b9228bcb36c47058dc740696a9ddd1a' \
--data-raw '{
  "messages": [
    {
      "content": "You are a helpful assistant that provides clear and accurate book recommendations and explanations. Respond in a friendly, concise, and professional manner.",
      "role": "system"
    },
    {
      "content": "Provide book recommendations ha are similar to code geass.",
      "role": "user"
    }
  ],
  "model": "deepseek-chat",
  "frequency_penalty": 0,
  "max_tokens": 500,
  "presence_penalty": 0,
  "response_format": {
    "type": "text"
  },
  "stop": null,
  "stream": true,
  "stream_options": null,
  "temperature": 1,
  "top_p": 1,
  "tools": null,
  "tool_choice": "none",
  "logprobs": false,
  "top_logprobs": null
}'
```

```python

from openai import OpenAI

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(api_key="<your API key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
  ],
    max_tokens=1024,
    temperature=0.7,
    stream=False
)

print(response.choices[0].message.content)
```

The system will process the query, retrieve the relevant book details, construct a prompt with that context, and stream back a JSON array of recommendations.

```json
data: {"id":"7e2b0ecf-a196-49a3-b783-d66076865d99","object":"chat.completion.chunk","created":1739834834,"model":"deepseek-chat","system_fingerprint":"fp_3a5770e1b4","choices":[{"index":0,"delta":{"role":"assistant","content":""},"logprobs":null,"finish_reason":null}]}

data: {"id":"7e2b0ecf-a196-49a3-b783-d66076865d99","object":"chat.completion.chunk","created":1739834834,"model":"deepseek-chat","system_fingerprint":"fp_3a5770e1b4","choices":[{"index":0,"delta":{"content":"If"},"logprobs":null,"finish_reason":null}]}

data: {"id":"7e2b0ecf-a196-49a3-b783-d66076865d99","object":"chat.completion.chunk","created":1739834834,"model":"deepseek-chat","system_fingerprint":"fp_3a5770e1b4","choices":[{"index":0,"delta":{"content":" you"},"logprobs":null,"finish_reason":null}]}

data: {"id":"7e2b0ecf-a196-49a3-b783-d66076865d99","object":"chat.completion.chunk","created":1739834834,"model":"deepseek-chat","system_fingerprint":"fp_3a5770e1b4","choices":[{"index":0,"delta":{"content":" enjoyed"},"logprobs":null,"finish_reason":null}]}

...

data: {"id":"7e2b0ecf-a196-49a3-b783-d66076865d99","object":"chat.completion.chunk","created":1739834834,"model":"deepseek-chat","system_fingerprint":"fp_3a5770e1b4","choices":[{"index":0,"delta":{"content":""},"logprobs":null,"finish_reason":"stop"}],"usage":{"prompt_tokens":19,"completion_tokens":940,"total_tokens":959,"prompt_tokens_details":{"cached_tokens":0},"prompt_cache_hit_tokens":0,"prompt_cache_miss_tokens":19}}

data: [DONE]

```
