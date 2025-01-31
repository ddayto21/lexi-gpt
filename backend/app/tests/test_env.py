import os

def test_load_env_vars_pytest_env():
    assert os.environ["API_URL"] == "http://localhost:8000"
