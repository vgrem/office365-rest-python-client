from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class AnalyticsItem(ClientValue):
    Id: str | None = None
    Properties: dict = field(default_factory=dict)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsItem"
