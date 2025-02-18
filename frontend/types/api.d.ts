export interface Book {
  title: string;
  author_name?: string[];
  description?: string;
  authors?: string[];
}

export interface SearchRequest {
  query: string;
}

export interface SearchResponse {
  recommendations: Book[];
  message?: string;
}

/**
 * Represents a single message in the conversation log
 */
export interface Message {
  role: string; // "user" | "assistant" | "system"
  content: string;
}


/** Represents the conversation history */

