from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.spark.category_score import SparkCategoryScore


class SparkCategorySimilarityResult(ClientValue):
    RequestId: str | None = None
    Scores: ClientValueCollection[SparkCategoryScore] = field(
        default_factory=lambda: ClientValueCollection(SparkCategoryScore)
    )
