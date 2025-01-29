export interface Book {
  cover_i?: number;
  has_fulltext?: boolean;
  edition_count?: number;
  title: string;
  author_name?: string[];
  first_publish_year?: number;
  key: string;
  author_key?: string[];
  public_scan_b?: boolean;
}

export interface BookSearchResponse {
  start: number;
  num_found: number;
  docs: Book[];
}
