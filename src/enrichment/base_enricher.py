"""Base interfaces for the product search MVP."""

from abc import ABC, abstractmethod

from base.models import EnrichedProduct


class Enricher(ABC):
    @abstractmethod
    def enrich(self, Product: dict) -> EnrichedProduct:
        """Transform raw events and tag metadata into enriched products."""

