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
