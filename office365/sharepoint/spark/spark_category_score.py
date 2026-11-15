from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SparkCategoryScore(ClientValue):
    Id: str | None = None
    Score: float | None = None
