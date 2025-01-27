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