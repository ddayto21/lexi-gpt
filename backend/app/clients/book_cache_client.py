# app/clients/book_cache_client.py

import json
import redis
import os
import logging


class CacheClient:
    """
    Provides caching for book search results in Redis.

    - Uses a default TTL of 3600 seconds (1 hour), but can be overridden.
    - Normalizes keys by trimming and lowercasing query strings.
    """

    def __init__(self, host=None, password=None, port=None, db=0, default_ttl=3600):
        self.host = host or os.getenv("REDIS_HOST", "redis")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.password = password or os.getenv("REDIS_PASSWORD", None)
        self.db = db
        self.default_ttl = default_ttl

        try:
            self.redis = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True,
            )
            self.ping_redis()
            logging.info(f"Connected to Redis at {self.host}:{self.port}")
        except redis.ConnectionError as e:
            logging.error(f"Failed to connect to Redis: {e}")
            self.redis = None  # Prevents failures in other methods

    def ping_redis(self):
        """Check if caching service is available."""

        if self.redis:
            try:
                return self.redis.ping()
            except redis.ConnectionError as e:
                logging.error(f"Failed to ping Redis: {e}")
                return False

    def _normalize_key(self, query: str) -> str:
        """
        Normalize a query string for consistent caching.
        """
        return query.strip().lower()

    def get_books(self, query: str):
        """
        Retrieve cached books for the normalized query.
        Returns None if the key is not present.
        """
        key = self._normalize_key(query)
        cached_data = self.redis.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

    def set_books(self, query: str, books: list, ttl: int = None):
        """
        Store a list of books under a normalized query key with an optional TTL.
        If no TTL is provided, uses the default_ttl.
        """
        key = self._normalize_key(query)
        data = json.dumps(books)
        self.redis.setex(key, ttl or self.default_ttl, data)

    def invalidate(self, query: str):
        """
        Explicitly remove the cached entry for a given query.
        """
        key = self._normalize_key(query)
        self.redis.delete(key)

    def ttl(self, query: str) -> int:
        """
        Return the current TTL for the given query key, or -2 if it doesn't exist.
        """
        key = self._normalize_key(query)
        return self.redis.ttl(key)
