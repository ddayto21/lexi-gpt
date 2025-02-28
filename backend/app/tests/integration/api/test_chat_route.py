# test_chat.py
import json
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.chat import router, SSEPayload, SSEErrorPayload

app = FastAPI()
app.include_router(router)
client = TestClient(app)


# Define dummy classes to mimic the expected DeepSeek API response structure.
class DummyDelta:
    def __init__(self, content: str):
        self.content = content


class DummyChoice:
    def __init__(self, content: str):
        self.delta = DummyDelta(content)


class DummyChunk:
    def __init__(self, content: str):
        self.choices = [DummyChoice(content)]


def dummy_stream():
    # Yield a series of DummyChunk objects to simulate the streaming response.
    for text in ["Hello", " ", "World!"]:
        yield DummyChunk(text)


def test_chat_streaming_success(monkeypatch):
    # Monkey-patch the DeepSeek API call to return our dummy stream.
    monkeypatch.setattr(
        "app.api.chat.client.chat.completions.create", lambda **kwargs: dummy_stream()
    )

    payload = {
        "messages": [
            {
                "id": "1",
                "role": "assistant",
                "content": "Initial message",
                "createdAt": "2025-02-19T12:00:00Z",
            },
            {
                "id": "2",
                "role": "user",
                "content": "Hello",
                "createdAt": "2025-02-19T12:00:05Z",
            },
        ]
    }

    response = client.post("/chat", json=payload)

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

    collected_text = ""
    for line in response.iter_lines():
        if not line:
            continue
        # The TestClient returns str, so no need to decode.
        decoded_line = line.strip()
        # Each SSE event should start with "data: "
        assert decoded_line.startswith("data: ")
        json_part = decoded_line[len("data: ") :].strip()
        try:
            event_data = json.loads(json_part)
        except json.JSONDecodeError:
            pytest.fail("Received invalid JSON in stream event.")
        try:
            # Using model_validate in Pydantic V2+ is preferred; adjust accordingly if needed.
            payload_obj = SSEPayload.parse_obj(event_data)
            collected_text += payload_obj.content
        except Exception:
            try:
                error_obj = SSEErrorPayload.parse_obj(event_data)
                pytest.fail(f"Received error event in stream: {error_obj.error}")
            except Exception as ve:
                pytest.fail(f"Stream event did not match expected schemas: {ve}")

    assert collected_text == "Hello World!"


def test_chat_invalid_payload():
    payload = {"invalid": "data"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 400
    json_response = response.json()
    assert "detail" in json_response
    assert "messages" in json_response["detail"]
