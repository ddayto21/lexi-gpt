def contains_profanity(query: str) -> bool:
    prohibited_words = ["badword"]
    return any(word in query.lower() for word in prohibited_words)