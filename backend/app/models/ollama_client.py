import asyncio
from ollama import AsyncClient


async def extract_keywords(query):
    prompt = (
        "You are a helpful assistant that extracts relevant keywords from user queries. "
        "When given a query, extract the key terms that best represent the main ideas and "
        "return them as a single, comma-separated string. Do not include any additional text."
    )

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": query},
    ]

    response = await AsyncClient().chat(model="llama3.2", messages=messages)
    return response.message.content


# Example usage
query = "I am looking for a book about the history of the Roman Empire."
keywords = asyncio.run(extract_keywords(query))
print(keywords)
