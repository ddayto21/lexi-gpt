import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import httpx


class LLMProvider(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, model: str, stream: bool, **kwargs) -> str:
        """
        Generate text using the given prompt, model, and streaming option.
        """
        pass


class DeepSeekAPIClient(LLMProvider):
    def __init__(
        self, api_key: str, base_url: str = "https://api.deepseek.com/chat/completions"
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        # Create persistent HTTP/2 client for reusable connections.
        self.client = httpx.Client(http2=True, timeout=httpx.Timeout(None))

    def generate_text(
        self, prompt: str, model: str = "deepseek-chat", stream: bool = False, **kwargs
    ) -> str:
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": model,
            "stream": stream,
        }
        payload.update(kwargs)

        response = self.client.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()

        # For non-streamed responses, parse and return the generated text
        if not stream:
            data = response.json()
            return self.parse_response(data)

        # For streamed responses, return the raw text response
        # Handle streaming as needed in the future
        return response.text

    def parse_response(self, data: dict) -> str:
        """
        Extract the generated text content from the DeepSeek API response.
        """
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("No choices found in response")

        message = choices[0].get("message", {})
        content = message.get("content", "")
        if not content:
            raise ValueError("No content found in response")
        return content

    def close(self):
        """Close the underlying HTTP client."""
        self.client.close()


if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("DEEPSEEK_API_KEY")

    # Ensure the API key was loaded successfully
    if not API_KEY:
        raise ValueError(
            "API key not found. Please set DEEPSEEK_API_KEY in your environment."
        )
    client = DeepSeekAPIClient(api_key=API_KEY)

    prompt = "Provide 5 book recommendations."
    response = client.generate_text(prompt, model="deepseek-chat", stream=True)
    print(response)
