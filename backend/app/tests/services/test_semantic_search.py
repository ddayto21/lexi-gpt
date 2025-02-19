import pytest
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from app.services.semantic_search import (
    create_vector_embedding,
    calculate_similarity_scores,
    get_top_k_books,
)


@pytest.fixture
def setup_fixture():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Load model
    device = "cpu" if not torch.cuda.is_available() else "cuda"
    yield model, device


@pytest.mark.parametrize(
    "text",
    [
        "A biographical novel about the life of Albert Einstein",
        "A historical fiction story set in ancient Greece",
        "A romance novel with a strong female protagonist",
        "A science fiction epic exploring intergalactic travel",
        "",
        "A humorous mystery novel featuring a detective",
        "A young adult fantasy series with magical realism elements",
        "A collection of short stories by Harper Lee",
        "A historical non-fiction book about the American Civil War",
    ],
)
def test_create_vector_embedding(text, setup_fixture):
    model, device = setup_fixture
    embedding = create_vector_embedding(model, device)
    print("Embedding shape:", embedding.shape)

    # Assertions
    assert isinstance(embedding, np.ndarray), "Output should be a NumPy array"
    assert embedding.shape[0] == 1, "Output should have batch size of 1"
    assert embedding.shape[1] > 0, "Embedding should have multiple dimensions"

    # Embedding should have 384 dimensions
    assert embedding.shape[1] == 384, "Embedding should have 384 dimensions"
    assert embedding.dtype == np.float32, "Embedding should be of type float32"


@pytest.mark.parametrize(
    "query,documents",
    [
        (
            "A science fiction novel",
            ["A futuristic space adventure", "A historical drama", "A book about AI"],
        ),
        (
            "A detective mystery",
            ["A crime thriller", "A love story", "A biography of Sherlock Holmes"],
        ),
        (
            "A book on machine learning",
            ["A deep learning guide", "A cooking recipe", "An autobiography"],
        ),
        ("", ["A physics textbook", "A novel about time travel", "A horror story"]),
    ],
)
def test_calculate_similarity_scores(query, documents, setup_fixture):
    model, device = setup_fixture

    # Generate embeddings
    query_embedding = create_vector_embedding(model, query, device)
    document_embeddings = np.vstack(
        [create_vector_embedding(model, doc, device) for doc in documents]
    )

    # Compute similarity scores
    similarity_scores = calculate_similarity_scores(
        query_embedding, document_embeddings
    )

    # Assertions
    assert isinstance(
        similarity_scores, torch.Tensor
    ), "Output should be a PyTorch tensor"
    assert similarity_scores.shape == (
        1,
        len(documents),
    ), "Shape mismatch: Should be (1, num_documents)"
    assert similarity_scores.dtype == torch.float32, "Tensor should be of type float32"

    # Ensure similarity values are within valid range [-1, 1]
    assert (similarity_scores >= -1).all() and (
        similarity_scores <= 1
    ).all(), "Similarity scores should be between -1 and 1"


@pytest.mark.parametrize(
    "query,books_metadata,k",
    [
        (
            "How to become rich and successful",
            [
                {
                    "title": "teach rich",
                    "author": "ramit sethi",
                    "subjects": "finance, wealth, investment",
                    "year": "2019",
                    "book_id": "OL123456W",
                    "embedding_input": "Title: teach rich. Author: ramit sethi. Subjects: finance, wealth, investment. Year: 2019.",
                },
                {
                    "title": "science get rich financial success creative thought",
                    "author": "wallace d wattle",
                    "subjects": "finance, motivation, success",
                    "year": "1910",
                    "book_id": "OL789012W",
                    "embedding_input": "Title: science get rich financial success creative thought. Author: wallace d wattle. Subjects: finance, motivation, success. Year: 1910.",
                },
                {
                    "title": "improve communication skill",
                    "author": "alan barker",
                    "subjects": "communication, personal development",
                    "year": "2007",
                    "book_id": "OL345678W",
                    "embedding_input": "Title: improve communication skill. Author: alan barker. Subjects: communication, personal development. Year: 2007.",
                },
                {
                    "title": "rapid instructional design",
                    "author": "george m piskurich",
                    "subjects": "education, training, learning",
                    "year": "2005",
                    "book_id": "OL901234W",
                    "embedding_input": "Title: rapid instructional design. Author: george m piskurich. Subjects: education, training, learning. Year: 2005.",
                },
                {
                    "title": "foundation entrepreneurship economic development",
                    "author": "david harper",
                    "subjects": "entrepreneurship, business, economy",
                    "year": "2003",
                    "book_id": "OL567890W",
                    "embedding_input": "Title: foundation entrepreneurship economic development. Author: david harper. Subjects: entrepreneurship, business, economy. Year: 2003.",
                },
            ],
            3,  # Expect top 3 books
        )
    ],
)
def test_get_top_k_books(query, books_metadata, k, setup_fixture):
    model, device = setup_fixture

    # Generate embeddings using "embedding_input"
    query_embedding = create_vector_embedding(model, query, device)
    book_embeddings = np.vstack(
        [
            create_vector_embedding(model, book["embedding_input"], device)
            for book in books_metadata
        ]
    )

    # Compute similarity scores
    similarity_scores = calculate_similarity_scores(query_embedding, book_embeddings)

    # Ensure similarity scores tensor is valid
    assert similarity_scores.numel() > 0, "Similarity tensor should not be empty"

    # Ensure `k` is valid and does not exceed the number of books
    k = min(k, len(books_metadata))
    assert k > 0, "k must be greater than zero"

    # Retrieve top-k books
    top_books = get_top_k_books(similarity_scores, books_metadata, k)

    # Assertions
    assert isinstance(top_books, list), "Output should be a list"
    assert len(top_books) == k, f"Should return exactly {k} books"
    assert all(
        isinstance(book, dict) for book in top_books
    ), "Each item should be a dictionary"
