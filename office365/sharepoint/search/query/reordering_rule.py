from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ReorderingRule(ClientValue):
    """The ReorderingRule type contains information about how search results SHOULD be reordered if they met the
    condition."""

    Boost: int | None = None
    MatchType: int | None = None
    MatchValue: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.ReorderingRule"
