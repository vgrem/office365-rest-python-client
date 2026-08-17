from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AccessReviewReviewerScope(ClientValue):
    query: str | None = None
    queryRoot: str | None = None
    queryType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewReviewerScope"
