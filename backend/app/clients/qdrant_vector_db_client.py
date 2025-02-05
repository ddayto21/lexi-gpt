from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost", 
    port=6333  # default HTTP port
)

# Optionally check health by getting a list of collections
collections = client.get_collections()
print(collections)