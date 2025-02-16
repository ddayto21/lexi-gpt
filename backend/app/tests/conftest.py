import os
import pytest
from dotenv import find_dotenv, load_dotenv

# Skip the entire file if running in a CI environment
if os.getenv("CI", "false").lower() == "true":
    pytest.skip("Skipping tests in CI environment", allow_module_level=True)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """
    Automatically loads environment variables from `.env.tests` before running any tests.
    """
    env_file = find_dotenv(".env.tests")
    if env_file:
        load_dotenv(env_file)
        print(f"Loaded environment variables from {env_file}")
    else:
        print("⚠️ No .env.tests file found, using default environment variables.")


@pytest.fixture
def query_fixture():
    return "anime similar to hunter hunter"


@pytest.fixture
def retrieved_context_fixture():
    return [
        {
            "book_id": "OL8215153W",
            "title": "hunter x hunter",
            "author": "yoshihiro togashi",
            "subjects": "magic, hunter, graphic novel, fiction, competition psychology, comic book strip, comic_strip graphic novel manga general",
            "year": "1998",
            "embedding_input": "Title: hunter x hunter. Author: yoshihiro togashi. Subjects: magic, hunter, graphic novel, fiction, competition psychology, comic book strip, comic_strip graphic novel manga general. Year: 1998.",
        },
        {
            "book_id": "OL265501W",
            "title": "wild",
            "author": "erin hunter",
            "subjects": "cat, fantasy, fantasy fiction, feral cat, fiction, juvenile fiction, children fiction, cat fiction, courage fiction, action, courage, adventure adventurer fiction, animal fiction, serieswarriorsthepropheciesbegin",
            "year": "2003",
            "embedding_input": "Title: wild. Author: erin hunter. Subjects: cat, fantasy, fantasy fiction, feral cat, fiction, juvenile fiction, children fiction, cat fiction, courage fiction, action, courage, adventure adventurer fiction, animal fiction, serieswarriorsthepropheciesbegin. Year: 2003.",
        },
        {
            "book_id": "OL8212073W",
            "title": "inuyasha",
            "author": "rumiko takahashi",
            "subjects": "good evil, magic, teenage girl, history, fiction, japan, hero, time travel, legend, manga, young adult literature, juvenile literature, comic_strip graphic novel east asian style manga science fiction, comic_strip graphic novel east asian style manga fantasy, comic_strip graphic novel east asian style manga romance, friendship fiction, comic_strip graphic novel east asian style manga historical fiction, comic_strip graphic novel east asian style manga crime mystery",
            "year": "1998",
            "embedding_input": "Title: inuyasha. Author: rumiko takahashi. Subjects: good evil, magic, teenage girl, history, fiction, japan, hero, time travel, legend, manga, young adult literature, juvenile literature, comic_strip graphic novel east asian style manga science fiction, comic_strip graphic novel east asian style manga fantasy, comic_strip graphic novel east asian style manga romance, friendship fiction, comic_strip graphic novel east asian style manga historical fiction, comic_strip graphic novel east asian style manga crime mystery. Year: 1998.",
        },
        {
            "book_id": "OL5714278W",
            "title": "long shadow",
            "author": "erin hunter",
            "subjects": "cat, fantasy, fantasy fiction, feral cat, fiction, juvenile fiction, children fiction, cat fiction, brother sister fiction, adventure adventurer fiction, brother sister, adventure adventurer, serieswarriorsthepowerofthree",
            "year": "2008",
            "embedding_input": "Title: long shadow. Author: erin hunter. Subjects: cat, fantasy, fantasy fiction, feral cat, fiction, juvenile fiction, children fiction, cat fiction, brother sister fiction, adventure adventurer fiction, brother sister, adventure adventurer, serieswarriorsthepowerofthree. Year: 2008.",
        },
        {
            "book_id": "OL5714292W",
            "title": "forest secret",
            "author": "erin hunter",
            "subjects": "cat, fantasy, fantasy fiction, feral cat, fiction, juvenile fiction, children fiction, cat fiction, courage, english fantasy fiction, adventure adventurer fiction, serieswarriorsthepropheciesbegin",
            "year": "2003",
            "embedding_input": "Title: forest secret. Author: erin hunter. Subjects: cat, fantasy, fantasy fiction, feral cat, fiction, juvenile fiction, children fiction, cat fiction, courage, english fantasy fiction, adventure adventurer fiction, serieswarriorsthepropheciesbegin. Year: 2003.",
        },
    ]


@pytest.fixture
def summaries_fixture():
    return [
        "hunter x hunter by yoshihiro togashi (1998). Keywords: magic, hunter, graphic novel",
        "wild by erin hunter (2003). Keywords: cat, fantasy, fantasy fiction",
        "inuyasha by rumiko takahashi (1998). Keywords: good evil, magic, teenage girl",
        "long shadow by erin hunter (2008). Keywords: cat, fantasy, fantasy fiction",
        "forest secret by erin hunter (2003). Keywords: cat, fantasy, fantasy fiction",
    ]


@pytest.fixture
def prompt_fixture(query_fixture, summaries_fixture) -> str:
    """
    Returns the prompt string constructed from the query and book summaries.
    """
    from app.services.rag_pipeline import construct_model_prompt

    return construct_model_prompt(query_fixture, summaries_fixture)


@pytest.fixture
def messages_fixture(prompt_fixture) -> list:
    """
    Returns the conversation messages constructed from the prompt.
    """
    from app.services.rag_pipeline import construct_messages

    return construct_messages(prompt_fixture)
