# Book Search Web Application

## Description

A responsive web application that allows users to search for books using natural language queries. The backend integrates with the OpenLibrary API and a Large Language Model (LLM) to process queries and provide enhanced book recommendations. This project demonstrates modern full-stack development and AI/ML integration.

## 1. System Requirements

- Objective: Build a web application that allows users to search for books using natural language queries.

- Key Components:
  - Frontend: A user-friendly interface for entering queries and displaying results.
  - Backend: A Python-based service that integrates with OpenLibrary and an LLM to process queries and generate natural language responses.
- Key Features:
  - Natural language query processing
  - Integration with OpenLibrary for book data
  - LLM-enhanced responses (e.g., summarizing book descriptions, generating recommendations).
  - Error handling and moderation (e.g., profanity filtering).

## 2. High-Level Architecture

The application will follow a client-server architecture:

- Frontend: A React-based web interface.
- Backend: A Python Flask/FastAPI service.
- External Services:
  - OpenLibrary: For fetching book metadata.
  - LLM: For query understanding, response generation, and summarization (e.g., OpenAI GPT -or- Hugging Face model).
- Database: Cache book data and store user queries

Database: Optional (e.g., for caching book data or storing user queries).

## 3. Frontend Implementation

- Tech Stack: React (for UI), HTML/CSS (for styling), Fetch API

### Features

- Search Bar: Allows users to enter natural language queries (e.g., "Find me a mystery novel set in Paris").
- Speech-to-Text: Optional feature for voice input.
- Results Display: Show book recommendations with titles, authors, and summaries in natural language.
- Interactive Filters: Allow users to refine results by genre, author, or publication year.
- Book Previews: Show book covers and allow users to click for more details.
- Responsive Design: Ensure the UI works seamlessly on both desktop and mobile devices.
- Loading States: Display a spinner or progress bar while fetching results.
- Error Handling: Show user-friendly messages for errors (e.g., "No results found" or "Service unavailable").

## 4. Backend Implementation

- Tech Stack: Python (Flask/FastAPI), Docker (for containerization), LLM API (e.g., OpenAI GPT).

### Services

- Query Understanding: The LLM extracts keywords and intent from the user's natural language query. (e.g., "mystery novel set in Paris" → genre: mystery, location: Paris).

- Information Retrieval: We use `OpenLibrary` to fetch relevant book data.
- /search-books (POST) that accepts a JSON payload with the user's query.

- Response Generation: The LLM summarizes book descriptoins and gneerates natural language responses.

- Format the response as a list of book recommendations with titles, authors, and summaries.
- Caching: Cache frequently searched queries to reduce latency.
- Personalization: Use session data to personalize recommendations (e.g., "Based on your previous searches, you might like...").

## 5. Integration with OpenLibrary and LLM

= Use the OpenLibrary Search API to fetch book data based on keywords extracted by the LLM.

- Example API call: https://openlibrary.org/search.json?q=mystery+paris.

## 6. Example Workflow

1. User Query: "Find me a mystery novel set in Paris with a strong female lead."

2. Backend Processing

- LLM extracts keywords: genre=mystery, location=Paris, character=strong female lead.

- OpenLibrary API fetches books matching these criteria.

- LLM summarizes the book descriptions and generates a natural language response.

3. Frontend Display

Display results:

"Here are some mystery novels set in Paris with strong female leads:"

"The Paris Apartment" by Lucy Foley - A gripping mystery set in a Parisian apartment building...

"The Elegance of the Hedgehog" by Muriel Barbery - A philosophical mystery featuring a strong female protagonist...

## Pre-Trained Large Language Models (LLMs)

To extract keywords from user query input, we will use pre-trained Large Language Models (LLMs) that are specifically designed for natural language understanding (NLU) tasks like `keyword extraction`, `intent detection`, and `entity recognition`.

Below are some specific LLMs and tools I considered using, along their tradeoffs.

### SpaCy (em_core_web_sm)

- I tried using `en_core_web_sm` for entity recognition, but didn't experience great results.

For example:

```python
nlp = spacy.load("en_core_web_sm")
doc = nlp("mystery novel set in Paris about a super hero")
keywords = [ent.text for ent in doc.ents]
```

The result was:

```stdout
['Paris']
```

### Open-Source Models

I decided to fine-tune a pre-trained model (e.g., BERT, GPT) on a dataset of book-related queries.

Example Dataset:

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

## Scientific Articles

- When to Retrieve: Teaching LLMs to Utilize Information Retrieval Effectively [arxiv](https://arxiv.org/abs/2404.19705)
- Large Language Models for Information Retrieval [arxiv](https://arxiv.org/pdf/2308.07107)
- Query Reformulation for Dynamic Information Integration [sci-hub](https://sci-hub.se/https://doi.org/10.1007/BF00122124)
- Analyzing and evaluating query reformulation strategies in web search logs (https://dl.acm.org/doi/abs/10.1145/1645953.1645966?casa_token=HARxSaPwK6QAAAAA:TBTQ4LyQO_34D_OikO6qyQx2ZrKZCotNyFApundsVYMDH3UrT6B7cFRVJAVNR08sBp7iSetubBy8)
- BM25 algorithm
- Webgpt: Browser-assisted question-answering with human feedback [arxiv](https://arxiv.org/abs/2112.09332)
- Improving language models by retrieving from trillions of tokens [International Conference on Machine Learning](https://arxiv.org/abs/2112.04426)
- MultiCoNER: A Large-scale Multilingual dataset for Complex Named Entity Recognition [arxiv](https://arxiv.org/abs/2208.14536)
- SemEval-2022 Task 11 on Multilingual Complex Named Entity Recognition (MultiCoNER) [acl](https://aclanthology.org/2022.semeval-1.196.pdf)
- Generalisation in named entity recognition: A quantitative analysis
- COGCOMPNLP: Your Swiss Army Knife for NLP (https://aclanthology.org/L18-1086.pdf): library used to simplify design and development process of NLP applications.
  - http://github.com/CogComp/cogcomp-nlp
  - search for text modules
- Query analysis with structural templates [Apple](https://dl.acm.org/doi/pdf/10.1145/3313831.3376451)
- Comparative Analysis of Neural QA models on SQuAD

## NER Datasets

- CoNLL03 (Sang and De Meulder, 2003) - Language-Independent Named Entity Recognition [PDF](https://aclanthology.org/W03-0419.pdf)

## Findings

Search Queries Dataset: ORCAS Dataset (Craswell et al., 2020)

- Human generated machine reading comprehension dataset

- Entity types (e.g., creative works) can be linguistically complex. They can be complex noun phrases (Eternal Sunshine of the Spotless Mind), gerunds (Saving Private Ryan), infinitives (To Kill a Mockingbird), or full clauses (Mr. Smith Goes to Washington). Syntactic parsing of such nouns is hard, and most current parsers and NER systems fail to recognize them

- MULTICONER (WNUT Taxonomy Entity Types)
- creative work entities (CREATIVE-WORK (CW, movie/song/book titles))

## Fine-Tuning

The objective is to fine-tune a BERT model for Named Entity Recognition (NER) for book search. This will require datasets containing labeled entities (e.g., `TITLE`, `AUTHOR`, `GENRE`).

Below is the approach I used to finding, curating, and preparing the best dataset for our use case.

### Search for Pre-Labeled NER Datasets

I searched for existing NER datasets that contain book-related entities, prioritizing datasets labeled with `titles`, `authors`, `genres`, `places`, and `publishers`.

### Hugging Face Datasets

https://huggingface.co/datasets

- bookcorpus - https://huggingface.co/datasets/bookcorpus/bookcorpus
- https://www.smashwords.com/
- Web Scraping: https://github.com/BIGBALLON/cifar-10-cnn

- Kaggle: Search for NER datasets for books, literature, or authors:

- Google Dataset Search

## Named Entity Recognition for Book Search

### Primary Entities to Extract

| **Entity Label** | **Description**                     | **OpenLibraryBook Field**            |
| ---------------- | ----------------------------------- | ------------------------------------ |
| `TITLE`          | Book title                          | `title`                              |
| `AUTHOR`         | Author name                         | `author_name`, `author_key`          |
| `GENRE`          | Book subject/category               | `subject`                            |
| `PUBLISHER`      | Publisher                           | `publisher`                          |
| `FORMAT`         | Book format (e.g., Paperback)       | `format`                             |
| `LANGUAGE`       | Language of the book                | `language`                           |
| `PLACE`          | Book setting or publishing location | `place`, `publish_place`             |
| `CHARACTER`      | Important book characters           | `person`                             |
| `YEAR`           | First publication year              | `first_publish_year`, `publish_year` |
| `ISBN`           | ISBN identifier                     | `isbn`                               |

---

### Example Training Data for Fine-Tuning

| **User Query**                                                    | **Labeled Entities**                                  |
| ----------------------------------------------------------------- | ----------------------------------------------------- |
| `"Find me a **mystery novel** by **Agatha Christie**"`            | `GENRE: "mystery novel"`, `AUTHOR: "Agatha Christie"` |
| `"Books published in **France** in **1990**"`                     | `PLACE: "France"`, `YEAR: "1990"`                     |
| `"Show books written in **Spanish**"`                             | `LANGUAGE: "Spanish"`                                 |
| `"Find **science fiction** books set in **Mars**"`                | `GENRE: "science fiction"`, `PLACE: "Mars"`           |
| `"Give me books by **J.K. Rowling** published by **Scholastic**"` | `AUTHOR: "J.K. Rowling"`, `PUBLISHER: "Scholastic"`   |

### Initialize React App

````bash
npx create-react-app frontend --use-yarn --template cra-template --skip-install```
````

## Install Swagger Editor CLI

```bash
yarn add swagger-cli --dev

```

### Validate Changes Consistently

As changes are made to the backend, revalidate the `openapi.yaml` file after any updates:

```bash
swagger-cli validate openapi.yaml

```

```bash
fastapi dev app/main.py
```

http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc

## Add TypeScript Support

```bash
yarn add typescript @types/react @types/react-dom
```

## OpenLibrary API

Examples

The URL format for API is simple. Take the search URL and add .json to the end. Eg:

    https://openlibrary.org/search.json?q=the+lord+of+the+rings
    https://openlibrary.org/search.json?title=the+lord+of+the+rings
    https://openlibrary.org/search.json?author=tolkien&sort=new
    https://openlibrary.org/search.json?q=the+lord+of+the+rings&page=2
    https://openlibrary.org/search/authors.json?q=twain

```
+----------------------------------------------------+
|  [Book Cover]    "The Lord of the Rings"          |
|                 by J.R.R. Tolkien                 |
|----------------------------------------------------|
| 🏆 250 Editions  📖 1193 Pages  🎙️ Audio Available |
| 🌎 Available in: EN, FR, SP, IT, DE...            |
| 📅 First Published: 1954                          |
| 🔖 Subjects: Fantasy, Middle-Earth, Magic         |
|----------------------------------------------------|
| 📥 Read Online  🔗 Borrow  ❤️ Add to Favorites    |
+----------------------------------------------------+
```

### Clickable Tags for Filtering

- Use auto-generated tags from subjects & characters.
- Clicking a tag refines search results dynamically.
