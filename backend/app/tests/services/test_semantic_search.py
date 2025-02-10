import pytest
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from app.services.semantic_search import create_vector_embedding


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
