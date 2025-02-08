import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
import json


model = SentenceTransformer("all-MiniLM-L6-v2")

# Load book embeddings (5121 books x 384 dimensions)
book_embeddings_file = "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/embedding_outputs.json"

book_embeddings_df = pd.read_json(book_embeddings_file)
print(book_embeddings_df.shape)
print(book_embeddings_df.head())


# Creates tensor with similar scores between the search query and the book embeddings
def calculate_similarity_scores(search_query):
    # Preprocess the search query
    search_query = search_query.lower()

    # Encode the search query
    search_query_embedding = model.encode([search_query]).astype("float32")

    # Convert dataframe to array for cosine similarity calculation
    embeddings_array = book_embeddings_df.to_numpy().astype("float32")

    similarities = util.cos_sim(search_query_embedding, embeddings_array)
    return similarities


def main():
    print("Running in main context")
    with open(
        "/Users/danieldayto/Projects/open-source-projects/book-search-web-app/backend/app/data/book_metadata/books_metadata.json",
        "r",
        encoding="utf-8",
    ) as file:
        books_metadata = json.load(file)

    search_query = "I am looking for an anime book with a genius mastermind protagonist that is cunning and manipulative "
    similarity_tensor = calculate_similarity_scores(search_query)
    print("similarity_tensor:", similarity_tensor)

    top_k = 5
    top_indices = np.argsort(similarity_tensor[0].cpu().numpy())[::-1][:top_k]

    print("top_indices:", top_indices)
    top_books = [books_metadata[i] for i in top_indices]
    print(
        "top related books:",
    )
    for book in top_books:
        print(f"{book['title']} by {book['author']}")


if __name__ == "__main__":
    main()
