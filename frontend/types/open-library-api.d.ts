

/**
 * Interface representing a book document returned by the Open Library API.
 */
export interface OpenLibraryBook {
  author_alternative_name?: string[];
  author_key?: string[];
  author_name?: string[];
  contributor?: string[];
  cover_edition_key?: string;
  cover_i?: number;
  ddc?: string[];
  ebook_access?: string;
  ebook_count_i?: number;
  edition_count?: number;
  edition_key?: string[];
  first_publish_year?: number;
  first_sentence?: string[];
  format?: string[];
  has_fulltext?: boolean;
  ia?: string[];
  ia_collection?: string[];
  ia_collection_s?: string;
  isbn?: string[];
  key: string;
  language?: string[];
  last_modified_i?: number;
  lcc?: string[];
  lccn?: string[];
  lending_edition_s?: string;
  lending_identifier_s?: string;
  number_of_pages_median?: number;
  oclc?: string[];
  osp_count?: number;
  printdisabled_s?: string;
  public_scan_b?: boolean;
  publish_date?: string[];
  publish_place?: string[];
  publish_year?: number[];
  publisher?: string[];
  ratings_average?: number;
  ratings_count?: number;
  readinglog_count?: number;
  want_to_read_count?: number;
  currently_reading_count?: number;
  already_read_count?: number;
  subject?: string[];
  place?: string[];
  time?: string[];
  person?: string[];
  title: string;
  title_sort?: string;
  title_suggest?: string;
  type?: string;
}

/**
 * Interface representing the API response for a book search.
 */
export interface OpenLibrarySearchResponse {
  numFound: number;
  start: number;
  numFoundExact: boolean;
  docs: OpenLibraryBook[];
}
