API Design

    Define a single POST /search-books operation in the openapi spec

    Use JSON schemas for request, response, and errors.

    The request body has a single property “query” (string).

    The response returns either a successful JSON with “recommendations” (an array of objects containing “title,” “authors,” and “description”) and possibly a top-level “message” for moderation warnings, or an error JSON if something fails.

    Include a “Book” model with fields “title” (string), “authors” (array of strings), and “description” (string). Define an “Error” model with “code” (string or integer) and “message” (string) for any issues like profanity detection or OpenLibrary/LLM failures. Specify 400 or 403 for validation/moderation errors, and 500 for system errors.

    Add documentation to describe LLM integration for query processing and response generation, and that the backend uses OpenLibrary based on the LLM-refined query.

Keep the latency requirement in mind: the spec can’t be overly complex or add extra synchronous calls.