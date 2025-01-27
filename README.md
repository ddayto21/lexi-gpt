# Book Search Web Application

## Description

A responsive web application that allows users to search for books using natural language queries. The backend integrates with the OpenLibrary API and a Large Language Model (LLM) to process queries and provide enhanced book recommendations. This project demonstrates modern full-stack development and AI/ML integration.

## Key Features

- Search for books using natural language queries.
- Backend processing with LLM to interpret and enhance queries.
- Integration with OpenLibrary API to fetch book data.
- Responsive and user-friendly frontend built with React.
- Caching for faster performance and reduced backend load.

## Application Structure

```
book-search-web-app/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   ├── public/
│   ├── package.json
│   └── README.md
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── main.py
│   └── requirements.txt
│   └── Dockerfile
│   └── README.md
├── README.md
```

### Initialize React App

````bash
npx create-react-app frontend --use-yarn --template cra-template --skip-install```
````

## Install Swagger Editor CLI

```bash
yarn add swagger-cli --dev

```
