# Book Recommendation System

## Overview

This project is a **Book Search Application** that allows users to search for books using natural language queries. The application integrates with the **OpenLibrary Web Service** to fetch book data and uses a **Large Language Model (LLM)** to process queries and generate natural language responses. The goal is to provide a fast, intuitive search experience with response times under **1-3 seconds**.

---

## Problem Statement

Users need a fast, intuitive way to search for books using natural language descriptions. The challenge is to build a system that can process these queries, fetch relevant data, and generate natural language responses within 1-3 seconds.

---

## Implementation Details

The application follows a **client-server architecture**:

### Frontend

- **Tech Stack**: React, Fetch API (for HTTP requests)
- **Core Features**:
  - **Smart Search**: Supports natural language queries for intuitive book discovery.
  - **Dynamic Recommendations**: Displays book titles, authors, and summaries based on user input.
  - **Responsive UI**: Optimized for both desktop and mobile devices.

---

## Implementation Details

### Frontend

- **Tech Stack**: React, Fetch API (for HTTP requests)
- **Core Features**:
  - **Smart Search**: Supports natural language queries for intuitive book discovery.
  - **Dynamic Recommendations**: Displays book titles, authors, and summaries based on user input.
  - **Responsive UI**: Optimized for both desktop and mobile devices.
- **Book Search**: Supports natural language queries for intuitive book discovery.
- **Dynamic Recommendations**: Displays book titles, authors, and summaries based on user input.
- **Responsive UI**: Optimized for both desktop and mobile devices.

### Backend

- **Tech Stack**:

  - **Python**: FastAPI
  - **Docker**: Containerization
  - **LLM API**: HF API, OpenAI API

- **Core Features**:

  - **Query Understanding**: The LLM extracts key details from user queries.

  - **Information Retrieval**: Calls the OpenLibrary API to fetch relevant book metadata.
  - **Response Generation**: Summarizes book descriptions and crafts natural language responses.
  - **Caching for Performance**: Frequently searched queries are cached, reducing API calls and improving response times.

### Pre-Trained Large Language Models (LLMs)

To extract keywords from user query input, we will use pre-trained Large Language Models (LLMs) that are specifically designed for natural language understanding (NLU) tasks like `keyword extraction`, `intent detection`, and `entity recognition`.

I decided to use a pre-trained model LLM on a dataset of book-related queries. Here’s an example of the dataset used:

```json
[
  {
    "query": "Find me a sci-fi book about space exploration.",
    "keywords": ["sci-fi", "space exploration"]
  },
  {
    "query": "I want a romance novel set in Italy.",
    "keywords": ["romance", "Italy"]
  }
]
```

## Scientific Articles and References

To ensure the application leverages the latest advancements in NLP and information retrieval, I referenced several scientific articles:

- When to Retrieve: Teaching LLMs to Utilize Information Retrieval Effectively ([arxiv](https://arxiv.org/abs/2404.19705))

- Large Language Models for Information Retrieval ([arxiv](https://arxiv.org/pdf/2308.07107))

- Query Reformulation for Dynamic Information Integration ([sci-hub](https://sci-hub.se/https://doi.org/10.1007/BF00122124))
