"""Read enriched products from disk and index them into OpenSearch."""

import argparse
import json
from pathlib import Path

from indexing.enriched_product_mapping import EnrichedProductMappingBuilder
from indexing.opensearch_client import OpenSearchClient
from indexing.opensearch_indexer import OpenSearchIndexer


def load_products(path: str) -> list[dict]:
    with Path(path).open("r", encoding="utf-8") as f:
        products = json.load(f)
    if not isinstance(products, list):
        raise ValueError("Enriched products file must contain a JSON array")
    return products


def main() -> None:
    parser = argparse.ArgumentParser(description="Index enriched products into OpenSearch")
    parser.add_argument("--input", required=True, help="Path to enriched products JSON file")
    parser.add_argument("--index", default="products", help="OpenSearch index name")
    parser.add_argument("--host", default="localhost", help="OpenSearch host")
    parser.add_argument("--port", type=int, default=9200, help="OpenSearch port")
    args = parser.parse_args()

    products = load_products(args.input)

    client = OpenSearchClient(host=args.host, port=args.port)
    indexer = OpenSearchIndexer(client)
    mapping_builder = EnrichedProductMappingBuilder()

    if not client.health_check():
        raise ConnectionError(f"OpenSearch is not reachable at {args.host}:{args.port}")

    indexer.create_index(args.index, mapping_builder.build())
    responses = indexer.bulk_index(args.index, products)

    print(f"Indexed {len(responses)} documents into '{args.index}' from {args.input}")


if __name__ == "__main__":
    main()
