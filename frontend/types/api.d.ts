// src/types/api.d.ts
export interface Book {
  title: string;
  author: string;
  summary: string;
}

export interface SearchBooksResponse {
  recommendations: Book[];
}
