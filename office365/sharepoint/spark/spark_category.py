from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SparkCategory(ClientValue):
    id: str | None = None
    text: str | None = None
