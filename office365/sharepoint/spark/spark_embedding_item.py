from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class SparkEmbeddingItem(ClientValue):
    Embedding: ClientValueCollection[float] = field(default_factory=ClientValueCollection)
    Index: int | None = None
