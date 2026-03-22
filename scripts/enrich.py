"""Minimal enrichment data model and interface."""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field


@dataclass
class PopularitySignals:
    views: int = 0
    carts: int = 0
    sales: int = 0
    returns: int = 0


@dataclass
class EnrichedProduct:
    product_id: str
    name: str
    category: str
    brand: str | None = None
    price: float = 0.0
    locale: str = "en-US"
    tags: list[str] = field(default_factory=list)
    synonyms: list[str] = field(default_factory=list)
    search_keywords: list[str] = field(default_factory=list)
    semantic_text: str = ""
    popularity: PopularitySignals = field(default_factory=PopularitySignals)
    last_event_timestamp: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


class Enricher(ABC):
    @abstractmethod
    def enrich(self, raw_events: list[dict], tags: dict) -> list[EnrichedProduct]:
        """Transform raw events and tag metadata into enriched products."""


class ProductEnricher(Enricher):
    def enrich(self, raw_events: list[dict], tags: dict) -> list[EnrichedProduct]:
        raise NotImplementedError("ProductEnricher.enrich is not implemented yet")


def main() -> None:
    print("Enrichment model ready")


if __name__ == "__main__":
    main()
