import json
import re
import logging
import spacy
from sentence_transformers import SentenceTransformer

# Dataset size:  5121
logging.basicConfig(level=logging.INFO)

# poetry run python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")


def normalize_text(text: str) -> str:
    """
    Normalize text by converting to lowercase, removing special characters, and extra whitespace.
    Then, tokenize, lemmatize, and remove stopwords using spaCy.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = " ".join(text.split())  # remove extra whitespace
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(tokens)

def subjects_to_string(subjects) -> str:
    """
    Converts subjects to a comma-separated string after normalizing each subject.
    If 'subjects' is a string, it splits on commas; if it's a list, it uses it directly.
    """
    if isinstance(subjects, str):
        subjects_list = [s.strip() for s in subjects.split(",")]
    elif isinstance(subjects, list):
        subjects_list = subjects
    else:
        subjects_list = []
    
    normalized_subjects = [normalize_text(subject) for subject in subjects_list if isinstance(subject, str)]
    return ", ".join(normalized_subjects)


def preprocess_book(book: dict) -> dict:
    """
    Preprocess a book document by normalizing its core fields:
      - title
      - author
      - subjects
      - year
    Returns a new dictionary with the normalized values.
    """
    normalized_book = {}
    
    normalized_book["title"] = normalize_text(book.get("title", ""))
    
    # Normalize author; join multiple authors if provided.
    authors = book.get("author", [])
    if isinstance(authors, list):
        normalized_book["author"] = normalize_text(", ".join(authors))
    elif isinstance(authors, str):
        normalized_book["author"] = normalize_text(authors)
    else:
        normalized_book["author"] = ""
    
    # Process subjects
    subjects = book.get("subjects", "")
    if isinstance(subjects, str):
        subjects_list = [s.strip() for s in subjects.split(",")]
    elif isinstance(subjects, list):
        subjects_list = subjects
    else:
        subjects_list = []
    normalized_book["subjects"] = subjects_to_string(subjects_list)
    
    # Process year
    year = book.get("year")
    normalized_book["year"] = str(year) if year is not None else ""
    
    # Retain book_id as is
    normalized_book["book_id"] = book.get("book_id", "")
    
    return normalized_book


def create_embedding_input(book: dict) -> str:
    """
    Combines the normalized fields into a single text string for the document embedding input.
    """
    return (
        f"Title: {book['title']}. "
        f"Author: {book['author']}. "
        f"Subjects: {book['subjects']}. "
        f"Year: {book['year']}."
    )


def create_vector_embeddings(books: list) -> list:
    """
    Generate vector embeddings for a list of books using a pre-trained SentenceTransformer model.
    """
    model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")
    embeddings = model.encode(books)
    return embeddings


    
    
def preprocess_main():
    input_file = "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/vector_data.json"
    embedding_inputs_file = "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/embedding_inputs.json"
    preprocessed_output_file = "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/preprocessed_vector_data.json"
    
    # Load the dataset (assumed to be a list of book objects)
    with open(input_file, "r", encoding="utf-8") as file:
        dataset = json.load(file)
    
    preprocessed_books = []
    embedding_inputs = []
    
    for book in dataset:
        preprocessed = preprocess_book(book)
        preprocessed_books.append(preprocessed)
        embedding_inputs.append(create_embedding_input(preprocessed))
    
    logging.info(f"Preprocessed {len(preprocessed_books)} books.")
    
    # Save embedding inputs to a file.
    with open(embedding_inputs_file, "w", encoding="utf-8") as file:
        json.dump(embedding_inputs, file, indent=4)
    logging.info(f"Saved embedding inputs to {embedding_inputs_file}")
    
    # Save the full preprocessed book data as well.
    with open(preprocessed_output_file, "w", encoding="utf-8") as file:
        json.dump(preprocessed_books, file, indent=4)
    logging.info(f"Saved preprocessed book data to {preprocessed_output_file}")
 


# Add textual book embedding to books metadata
# - for each book in the "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/preprocessed_vector_data.json" file
#    - add textual embedding to the book object
#     (textual book embedding is found in "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/embedding_inputs.json" file)
# For each textual book embedding in "embedding_inputs.json" file, add it to the corresponding book object in "preprocessed_vector_data.json" file.
# Ensure the length of items in the preprocessed_vector_data.json file is the same as the length of items in the embedding_inputs.json file.
def add_embedding_input_to_book_metadata():
    preprocessed_books_file = "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/preprocessed_vector_data.json"
    embedding_inputs_file = "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/embedding_inputs.json"
    output_file = "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/books_metadata.json"
    
    with open(preprocessed_books_file, "r", encoding="utf-8") as file:
        preprocessed_books = json.load(file)
    
    with open(embedding_inputs_file, "r", encoding="utf-8") as file:
        embedding_inputs = json.load(file)
    
    if len(preprocessed_books) != len(embedding_inputs):
        logging.error("Length of preprocessed books and embedding inputs do not match.")
        return
    
    for i, book in enumerate(preprocessed_books):
        book["embedding_input"] = embedding_inputs[i]
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(preprocessed_books, file, indent=4)
    logging.info(f"Saved book metadata with embedding inputs to {output_file}")
    

def main_create_embeddings():
    input_file = "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/embedding_inputs.json"
    output_file = "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/embedding_outputs.json"
    
    # Load pre-trained embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    
    
    # Load the embedding inputs
    with open(input_file, "r", encoding="utf-8") as file:
        books = json.load(file)
    
    vector_embeddings = model.encode(books)

    
    # Save the embeddings to a file
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(vector_embeddings.tolist(), file, indent=4)
    logging.info(f"Saved vector embeddings to {output_file}")
            

if __name__ == "__main__":
    add_embedding_input_to_book_metadata()


# tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
# text = "Replace me by any text you'd like."
# encoded_input = tokenizer(text, return_tensors='pt')
# print(encoded_input)
# """

#     DistilBERT-BookCorpus : DistilBERT is a smaller, more efficient version of BERT that still achieves impressive results. The BookCorpus variant of DistilBERT could also be a good choice for generating embeddings on resource-constrained hardware.

# """

# # model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")
