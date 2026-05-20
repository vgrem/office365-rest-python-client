from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AnalyticsActor(ClientValue):
    Id: str | None = None
    Properties: dict = field(default_factory=dict)
    TenantId: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsActor"
