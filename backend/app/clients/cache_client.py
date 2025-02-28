# app/clients/cache_client.py
import json
import redis
import os
import logging
from typing import Optional, Any, Dict, Union


class CacheClient:
    """
    A flexible Redis caching client for storing and retrieving data.

    Designed to cache various types of data (e.g., book search results, user profiles) with
    configurable TTLs. Normalizes keys for consistency and provides methods for both
    ephemeral and persistent storage.

    Attributes:
        host (str): Redis server hostname (default from REDIS_HOST env or "redis").
        port (int): Redis server port (default from REDIS_PORT env or 6379).
        password (str): Redis password (default from REDIS_PASSWORD env or None).
        db (int): Redis database number (default 0).
        default_ttl (int): Default time-to-live in seconds for cached items (default 3600).
        redis (redis.Redis): The Redis connection instance, or None if connection fails.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        password: Optional[str] = None,
        db: int = 0,
        default_ttl: int = 3600,
    ) -> None:
        """Initialize the Redis client with environment-based or explicit configuration."""
        self.host = host or os.getenv("REDIS_HOST", "redis")
        self.port = port or int(os.getenv("REDIS_PORT", "6379"))
        self.password = password or os.getenv("REDIS_PASSWORD", None)
        self.db = db
        self.default_ttl = default_ttl

        # Attempt to establish Redis connection
        try:
            self.redis = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True,  # Return strings instead of bytes
            )
            if self.is_healthy():
                logging.info(
                    f"Redis connected at {self.host}:{self.port}, db={self.db}"
                )
            else:
                raise redis.ConnectionError("Ping failed")
        except redis.ConnectionError as e:
            logging.error(f"Redis connection failed: {e}")
            self.redis = None  # Fallback to avoid crashes; methods will check this

    def is_healthy(self) -> bool:
        """
        Check if the Redis connection is active by sending a PING command.

        Returns:
            bool: True if Redis responds, False otherwise.
        """
        if not self.redis:
            return False
        try:
            return self.redis.ping()
        except redis.ConnectionError as e:
            logging.error(f"Redis health check failed: {e}")
            return False

    def _normalize_key(self, key: str) -> str:
        """
        Normalize a cache key by trimming whitespace and converting to lowercase.

        Args:
            key (str): The raw key string.

        Returns:
            str: The normalized key for consistent caching.
        """
        return key.strip().lower()

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a cached value by key, deserializing JSON if present.

        Args:
            key (str): The cache key (normalized internally).

        Returns:
            Any: Deserialized data if found, None if key doesn’t exist or Redis is down.
        """
        if not self.redis:
            logging.warning("Redis unavailable; skipping cache get")
            return None
        normalized_key = self._normalize_key(key)
        try:
            data = self.redis.get(normalized_key)
            return json.loads(data) if data else None
        except (redis.RedisError, json.JSONDecodeError) as e:
            logging.error(f"Cache get failed for key {normalized_key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Store a value in the cache with an optional TTL, serializing to JSON.

        Args:
            key (str): The cache key (normalized internally).
            value (Any): The data to cache (must be JSON-serializable).
            ttl (int, optional): Time-to-live in seconds; uses default_ttl if None.

        Returns:
            bool: True if successful, False if Redis is unavailable or operation fails.
        """
        if not self.redis:
            logging.warning("Redis unavailable; skipping cache set")
            return False
        normalized_key = self._normalize_key(key)
        try:
            data = json.dumps(value)
            self.redis.setex(normalized_key, ttl or self.default_ttl, data)
            return True
        except redis.RedisError as e:
            logging.error(f"Cache set failed for key {normalized_key}: {e}")
            return False

    def set_hash(self, key: str, data: Dict[str, str]) -> bool:
        """
        Store a dictionary as a Redis hash under the given key (no TTL by default).

        Args:
            key (str): The hash key (not normalized, as it’s typically a unique ID).
            data (Dict[str, str]): Key-value pairs to store in the hash.

        Returns:
            bool: True if successful, False if Redis is unavailable or operation fails.
        """
        if not self.redis:
            logging.warning("Redis unavailable; skipping hash set")
            return False
        try:
            self.redis.hset(key, mapping=data)
            return True
        except redis.RedisError as e:
            logging.error(f"Hash set failed for key {key}: {e}")
            return False

    def get_hash(self, key: str) -> Optional[Dict[str, str]]:
        """
        Retrieve all fields from a Redis hash by key.

        Args:
            key (str): The hash key.

        Returns:
            Dict[str, str]: The hash data if found, None if key doesn’t exist or Redis is down.
        """
        if not self.redis:
            logging.warning("Redis unavailable; skipping hash get")
            return None
        try:
            return self.redis.hgetall(key) or None
        except redis.RedisError as e:
            logging.error(f"Hash get failed for key {key}: {e}")
            return None

    def delete(self, key: str) -> bool:
        """
        Remove a key from the cache.

        Args:
            key (str): The cache key (normalized internally).

        Returns:
            bool: True if deleted or key didn’t exist, False if operation fails.
        """
        if not self.redis:
            logging.warning("Redis unavailable; skipping delete")
            return False
        normalized_key = self._normalize_key(key)
        try:
            self.redis.delete(normalized_key)
            return True
        except redis.RedisError as e:
            logging.error(f"Cache delete failed for key {normalized_key}: {e}")
            return False

    def get_ttl(self, key: str) -> int:
        """
        Get the remaining time-to-live for a key.

        Args:
            key (str): The cache key (normalized internally).

        Returns:
            int: TTL in seconds; -2 if key doesn’t exist, -1 if no expiration, or 0+ if expiring.
        """
        if not self.redis:
            logging.warning("Redis unavailable; returning -2 for TTL")
            return -2
        normalized_key = self._normalize_key(key)
        try:
            return self.redis.ttl(normalized_key)
        except redis.RedisError as e:
            logging.error(f"TTL check failed for key {normalized_key}: {e}")
            return -2
