
from base.models import EnrichedProduct, PopularitySignals
from .base_enricher import Enricher
import json
from pathlib import Path

class ProductEnricher(Enricher):

    def __init__(self, tags: dict) -> None:
        self.tags = tags

    def derive_tags(self, product: dict, tags: dict) -> tuple[str | None, list[str], list[str]]:
        tag_data = tags.get(product["product_id"], {})
        brand = tag_data.get("brand")
        labels = tag_data.get("labels", [])
        synonyms = tag_data.get("synonyms", [])
        return brand, labels, synonyms

    def build_search_text(self, product: dict, labels: list[str], synonyms: list[str]) -> tuple[list[str], str]:
        keywords = [
            product["name"].strip().lower(),
            product["category"].lower(),
            *[label.lower() for label in labels],
            *[synonym.lower() for synonym in synonyms],
        ]
        semantic_text = " ".join(keywords)
        return keywords, semantic_text

    def normalize_locale(self, product: dict) -> str:
        return product.get("locale", "en-US").strip()

    def enrich_product(self, product: dict) -> EnrichedProduct:
        brand, labels, synonyms = self.derive_tags(product, self.tags)
        search_keywords, semantic_text = self.build_search_text(product, labels, synonyms)
        locale = self.normalize_locale(product)

        return EnrichedProduct(
            product_id=product["product_id"],
            name=product["name"].strip(),
            category=product["category"],
            price=product["price"],
            locale=locale,
            brand=brand,
            tags=labels,
            synonyms=synonyms,
            search_keywords=search_keywords,
            semantic_text=semantic_text,
            popularity=PopularitySignals(),
            last_event_timestamp=product.get("timestamp", ""),
        )

    def enrich(self, raw_event: dict) -> EnrichedProduct:
        return self.enrich_product(raw_event)

