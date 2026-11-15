from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.spark.embedding_item import SparkEmbeddingItem


class SparkEmbeddingResult(ClientValue):
    Embeddings: ClientValueCollection[SparkEmbeddingItem] = field(
        default_factory=lambda: ClientValueCollection(SparkEmbeddingItem)
    )
    PromptTokens: int | None = None
    TotalTokens: int | None = None
