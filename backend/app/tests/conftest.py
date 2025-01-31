import pytest
from dotenv import find_dotenv, load_dotenv


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
