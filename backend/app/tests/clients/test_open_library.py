# tests/test_openlibrary_subjects.py

import pytest
import asyncio
from app.clients.open_library import OpenLibraryAPI

pytestmark = pytest.mark.asyncio  

# @pytest.mark.asyncio
# async def test_fetch_subject_data_minimal():
#     """
#     Tests the _fetch_subject_data method for a common subject like 'love'.
#     Should return a dict with 'works' and other keys.
#     """
#     api = OpenLibraryAPI()
#     data = await api._fetch_subject_data("love", details=False, limit=5)
#     assert isinstance(data, dict), "Expected a dictionary response"
#     assert "works" in data, "Expected 'works' key in response"
#     assert len(data["works"]) <= 5, "Should return up to 5 works"

# @pytest.mark.asyncio
# async def test_fetch_subject_data_details():
#     """
#     Tests the _fetch_subject_data method with 'details=true'.
#     Should return additional fields like 'authors', 'publishers', etc.
#     """
#     api = OpenLibraryAPI()
#     data = await api._fetch_subject_data("love", details=True, limit=5)
#     print("data", data)
#     assert isinstance(data, dict)
#     # Check if top-level authors/publishers exist
#     # They might not always appear, but typically 'details=true' yields them
#     # So we do a soft check.
#     if "authors" in data:
#         assert isinstance(data["authors"], list), "Authors should be a list if present"
#     if "publishers" in data:
#         assert isinstance(data["publishers"], list), "Publishers should be a list if present"

# @pytest.mark.asyncio
# async def test_fetch_subject_data_nonexisting():
#     """
#     Tests _fetch_subject_data for a subject key that likely doesn't exist.
#     We expect an empty dict or minimal structure.
#     """
#     api = OpenLibraryAPI()
#     # Something random, hopefully not a real subject
#     data = await api._fetch_subject_data("this_subject_should_not_exist_12345")
#     assert isinstance(data, dict), "Should return a dict, even if empty or minimal"
#     # Likely no 'works' key or 0 works
#     works = data.get("works", [])
#     assert len(works) == 0, "Expected no works for a nonexisting subject"

# @pytest.mark.asyncio
# async def test_fetch_subject_data_pagination():
#     """
#     Tests limit & offset functionality to ensure we can fetch
#     different slices of data.
#     """
#     api = OpenLibraryAPI()
#     data1 = await api._fetch_subject_data("fantasy", details=False, limit=2, offset=0)
#     data2 = await api._fetch_subject_data("fantasy", details=False, limit=2, offset=2)

#     assert "works" in data1 and "works" in data2
#     assert len(data1["works"]) <= 2
#     assert len(data2["works"]) <= 2

#     # Check if there's minimal overlap or difference
#     # It's possible they might overlap if the subject is small, but
#     # for "fantasy" there should be many works. We'll do a loose check.
#     keys1 = {w["key"] for w in data1["works"]}
#     keys2 = {w["key"] for w in data2["works"]}
#     # There's a chance of overlap, but let's see if they differ
#     # We won't assert strictly because it's real data
#     # but let's just confirm they are sets for debugging
#     assert isinstance(keys1, set) and isinstance(keys2, set)

# @pytest.mark.asyncio
# async def test_fetch_subject_expanded_no_expansion():
#     """
#     Tests fetch_subject_expanded with no expansions explicitly provided.
#     Should revert to a single subject fetch.
#     """
#     api = OpenLibraryAPI()
#     works, metadata = await api.fetch_subject_expanded(base_subject="love", limit=5)
#     # We expect some works
#     assert isinstance(works, list), "Should return a list of works"
#     assert len(works) <= 5, "We used limit=5, so should see up to 5"

#     # Check metadata structure
#     assert "authors" in metadata and "publishers" in metadata, "Expected authors/publishers keys in metadata"

# @pytest.mark.asyncio
# async def test_fetch_subject_expanded_with_expansion():
#     """
#     Tests fetch_subject_expanded with multiple expansions for concurrency.
#     We'll test expansions like ["love", "romantic love"].
#     """
#     api = OpenLibraryAPI()
#     expansions = ["love", "romantic love"]
#     works, metadata = await api.fetch_subject_expanded(
#         base_subject="love",
#         expansions=expansions,
#         details=True,
#         limit=5
#     )
#     print("metadata", metadata)
#     assert isinstance(works, list)
#     # We might have duplicates internally, but the method should deduplicate
#     # So the total length might be more or less than 5, 
#     # depending on overlap.
#     # We'll do a loose check that we get something:
#     assert len(works) > 0, "Expected some works from expansions"

#     # Check metadata
#     assert isinstance(metadata, dict)
#     assert "authors" in metadata and "publishers" in metadata

# @pytest.mark.asyncio
# async def test_fetch_subject_expanded_ebooks():
#     """
#     Tests fetch_subject_expanded with ebooks=True, ensuring we only get ebooks.
#     We'll pick a subject likely to have some ebooks, e.g. 'fantasy'.
#     """
#     api = OpenLibraryAPI()
#     works, metadata = await api.fetch_subject_expanded(
#         base_subject="fantasy",
#         details=True,
#         ebooks=True,
#         limit=5
#     )
#     # We should see works that hopefully have ebook versions
#     # The 'has_fulltext' might be True in many of them
#     assert len(works) > 0, "Expected some e-book results for fantasy"
#     for w in works:
#         # Usually 'has_fulltext' indicates there's an ebook available
#         # We do a soft check:
#         assert w.get("has_fulltext", False) is True, \
#             f"Work {w['key']} does not have fulltext, but ebooks=True was requested"