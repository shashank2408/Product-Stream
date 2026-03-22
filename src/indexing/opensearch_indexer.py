"""OpenSearch-backed indexer implementation."""

from indexing.base_indexer import BaseIndexer
from indexing.opensearch_client import OpenSearchClient


class OpenSearchIndexer(BaseIndexer):
    def __init__(self, client: OpenSearchClient) -> None:
        self.client = client

    def create_index(self, index_name: str, body: dict | None = None) -> dict:
        if self.client.client is None:
            self.client.connect()
        if self.client.client.indices.exists(index=index_name):
            return {"acknowledged": True, "message": f"Index '{index_name}' already exists"}
        return self.client.client.indices.create(index=index_name, body=body or {})

    def index_document(self, index_name: str, document: dict, document_id: str | None = None) -> dict:
        if self.client.client is None:
            self.client.connect()
        return self.client.client.index(index=index_name, body=document, id=document_id, refresh=True)

    def bulk_index(self, index_name: str, documents: list[dict]) -> list[dict]:
        responses: list[dict] = []
        for document in documents:
            document_id = document.get("product_id")
            responses.append(self.index_document(index_name, document, document_id=document_id))
        return responses

