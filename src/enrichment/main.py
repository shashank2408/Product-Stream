import json
from pathlib import Path
import argparse
from .product_enricher import ProductEnricher

def load_file(path: str) -> dict:
    try:
        with Path(path).open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise ValueError("Input file must be a JSON file and must be present in the path") from exc


def write_output(path: str, products: list[dict]) -> None:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run product enrichment")
    parser.add_argument("--input", required=True, help="Path to raw events JSON file")
    parser.add_argument("--tags", required=True, help="Path to tags JSON file")
    parser.add_argument("--output", required=True, help="Path to enriched output JSON file")

    args = parser.parse_args()

    product_events = load_file(args.input)
    tags = load_file(args.tags)

    enricher = ProductEnricher(tags)
    enriched_products = [enricher.enrich(event).to_dict() for event in product_events]

    write_output(args.output, enriched_products)
    print(f"Wrote {len(enriched_products)} enriched products to {args.output}")
